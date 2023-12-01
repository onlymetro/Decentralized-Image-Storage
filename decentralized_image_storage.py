from flask import Flask, render_template, request, jsonify
from web3 import Web3
import os

app = Flask(__name__)
images_directory = "images/"
blockchain = None

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
images_directory = "images/"

def create_images_directory():
    os.makedirs(images_directory, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"})

    filename = os.path.join(images_directory, file.filename)
    file.save(filename)

    return jsonify({"success": "Image uploaded successfully"})

@app.route('/images', methods=['GET'])
def get_images():
    image_files = [f for f in os.listdir(images_directory) if os.path.isfile(os.path.join(images_directory, f))]
    return jsonify({"images": image_files})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    create_images_directory()
    app.run(port=5000)

def create_images_directory():
    os.makedirs(images_directory, exist_ok=True)

def init_blockchain():
    global blockchain
    blockchain = Web3(Web3.EthereumTesterProvider())

    # Deploy a simple smart contract for image ownership
    contract_source_code = """
    pragma solidity ^0.8.0;

    contract ImageOwnership {
        address public owner;

        event ImageUploaded(string filename, address uploader);

        constructor() {
            owner = msg.sender;
        }

        function uploadImage(string memory filename) public {
            require(msg.sender == owner, "Only the owner can upload images");
            emit ImageUploaded(filename, msg.sender);
        }
    }
    """

    compiled_contract = blockchain.eth.compileSolidity(contract_source_code)
    contract_interface = compiled_contract['<stdin>:ImageOwnership']

    # Deploy the contract
    contract = blockchain.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    transaction_hash = contract.constructor().transact()
    transaction_receipt = blockchain.eth.waitForTransactionReceipt(transaction_hash)

    # Save the contract address for future interactions
    blockchain_contract_address = transaction_receipt['contractAddress']
    return blockchain_contract_address

@app.route('/upload', methods=['POST'])
def upload_image():
    # Existing code
    pass

@app.route('/images', methods=['GET'])
def get_images():
    # Existing code
    pass

@app.route('/')
def index():
    # Existing code
    pass

if __name__ == '__main__':
    create_images_directory()

    # Initialize the blockchain and get the contract address
    contract_address = init_blockchain()

    app.run(port=5000)