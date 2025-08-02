# Omni
Baddass dApp
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Parameter
from qiskit.visualization import plot_histogram, plot_state_city, plot_bloch_multivector
from qiskit.quantum_info import Operator, state_fidelity
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import requests
import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import json

load_dotenv()

PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_API_SECRET = os.getenv("PINATA_API_SECRET")

# --- Existing functions from your code ---
def add_variational_layer(circuit, qubits, theta, phi):
    for i in qubits:
        circuit.ry(theta, i)
        circuit.rz(phi, i)
    for i in range(len(qubits) - 1):
        circuit.cx(qubits[i], qubits[i + 1])

def omni_one_kernel_variational(n_qubits=5, phase_negfib=5, delta=0.5, layers=1, measure_all=False):
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_qubits, 'c') if measure_all else None
    circuit = QuantumCircuit(qr, cr) if measure_all else QuantumCircuit(qr)
    theta = Parameter('θ')
    phi = Parameter('φ')
    parameters = [theta, phi]
    circuit.h(range(n_qubits))
    circuit.rz(theta * phase_negfib * np.pi, 0)
    for i in range(n_qubits - 1):
        circuit.cx(i, i + 1)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.crz(phi * np.cos(delta * phase_negfib), 2, 3)
    circuit.h(4)
    circuit.cswap(4, 2, 3)
    for layer in range(layers):
        layer_theta = Parameter(f'θ_{layer}')
        layer_phi = Parameter(f'φ_{layer}')
        parameters.extend([layer_theta, layer_phi])
        add_variational_layer(circuit, range(n_qubits), layer_theta, layer_phi)
    if measure_all:
        circuit.measure(qr, cr)
    return circuit, parameters

def get_backend(backend_type='statevector', noisy=False):
    backend = AerSimulator(method=backend_type)
    if noisy and backend_type == 'qasm':
        noise_model = NoiseModel()
        error_1q = depolarizing_error(0.01, 1)
        error_2q = depolarizing_error(0.05, 2)
        noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'ry', 'rz', 'crz'])
        noise_model.add_all_qubit_quantum_error(error_2q, ['cx', 'cswap'])
        return backend, noise_model
    return backend, None

def simulate_circuit(circuit, backend_type='statevector', noisy=False, shots=1024, callback=None):
    backend, noise_model = get_backend(backend_type, noisy)
    try:
        result = backend.run(circuit, shots=shots, noise_model=noise_model).result()
        if callback:
            callback(result)
        if backend_type == 'statevector':
            statevector = result.get_statevector()
            prob_sum = np.sum(np.abs(statevector)**2)
            return {
                'statevector': statevector,
                'amplitudes': np.abs(statevector)[:10],
                'prob_sum': prob_sum
            }
        else:
            counts = result.get_counts()
            metadata = {'counts': counts, 'version': '1.0.0'}
            ipfs_uri = upload_kernel_metadata(metadata)
            return {'counts': counts, 'ipfs_uri': ipfs_uri}
    except Exception as err:
        return {'error': str(err)}

# --- New functions to complete the script ---

def upload_to_ipfs(file_path):
    """Uploads a file to Pinata and returns its IPFS URI."""
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://api.pinata.cloud/pinning/pinFileToIPFS",
            files={"file": (os.path.basename(file_path), f)},
            headers={"pinata_api_key": PINATA_API_KEY, "pinata_secret_api_key": PINATA_API_SECRET}
        )
    ipfs_hash = response.json()["IpfsHash"]
    return f"ipfs://{ipfs_hash}"

def upload_json_to_ipfs(json_data):
    """Uploads JSON data to Pinata and returns its IPFS URI."""
    response = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS",
        json=json_data,
        headers={"pinata_api_key": PINATA_API_KEY, "pinata_secret_api_key": PINATA_API_SECRET}
    )
    ipfs_hash = response.json()["IpfsHash"]
    return f"ipfs://{ipfs_hash}"

def build_and_sign_kernel(kernel_file="omni_one_kernel.py"):
    """
    Signs the quantum kernel file, uploads it to IPFS, and creates a verifiable metadata file.
    
    Args:
        kernel_file (str): The path to the kernel script to be signed.
        
    Returns:
        str: The IPFS URI for the signed metadata file.
    """
    # Generate RSA key pair (store securely)
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    # NOTE: You should securely store these keys in a real application, not write them to disk.
    # For this example, we'll write the public key to a file for easy access.
    with open("public_key.pem", "wb") as f:
        f.write(public_key_pem)

    print("🔹 New RSA key pair generated. Public key saved to public_key.pem.")

    # Upload kernel file to IPFS
    kernel_ipfs_uri = upload_to_ipfs(kernel_file)
    print(f"🔹 Quantum kernel uploaded to IPFS: {kernel_ipfs_uri}")
    
    # Sign the kernel file data
    with open(kernel_file, "rb") as f:
        kernel_data = f.read()
    signature = private_key.sign(
        kernel_data,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    signature_hex = signature.hex()

    # Create and upload verifiable metadata
    metadata = {
        "kernel_ipfs_uri": kernel_ipfs_uri,
        "signature": signature_hex,
        "public_key_pem": public_key_pem.decode('utf-8'),
        "version": "1.0.0"
    }
    metadata_ipfs_uri = upload_json_to_ipfs(metadata)
    print(f"🔹 Verifiable metadata uploaded to IPFS: {metadata_ipfs_uri}")
    
    return metadata_ipfs_uri

if __name__ == "__main__":
    # Example usage:
    # This will simulate and visualize results, but the main goal is to show the
    # kernel signing and uploading process.
    
    # First, let's create a kernel file to sign
    kernel_code = """
from qiskit import QuantumCircuit, QuantumRegister

def get_kernel_circuit():
    circuit = QuantumCircuit(3)
    circuit.h(range(3))
    circuit.cx(0, 1)
    circuit.rz(0.5, 2)
    return circuit
"""
    with open("omni_one_kernel_to_sign.py", "w") as f:
        f.write(kernel_code)

    print("--- Building and Signing Quantum Kernel ---")
    metadata_uri = build_and_sign_kernel(kernel_file="omni_one_kernel_to_sign.py")
    print("\n✅ Kernel build and sign process complete.")
    print(f"Use this metadata URI in your application to verify the kernel: {metadata_uri}")
