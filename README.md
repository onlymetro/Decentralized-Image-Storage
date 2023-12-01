# Decentralized-Image-Storage
This code is a Python script using the Flask web framework and the Web3 library for interacting with Ethereum. It provides a simple web application that allows users to upload images, view the list of uploaded images, and interact with a basic Ethereum smart contract for image ownership.

Let's break down the code:

Flask Setup:

python
Copy code
from flask import Flask, render_template, request, jsonify
from web3 import Web3
import os

app = Flask(__name__)
images_directory = "images/"
blockchain = None
This section imports necessary libraries, initializes a Flask app, sets the directory for storing uploaded images (images_directory), and declares a variable (blockchain) to store the Web3 instance later.

Flask Routes:

python
Copy code
@app.route('/upload', methods=['POST'])
def upload_image():
    # Handles image upload logic
    pass

@app.route('/images', methods=['GET'])
def get_images():
    # Retrieves the list of uploaded images
    pass

@app.route('/')
def index():
    # Renders the main HTML page
    pass
These are the Flask routes:

/upload: Handles image uploads.
/images: Retrieves the list of uploaded images.
/: Renders the main HTML page.
Image Directory Creation:

python
Copy code
def create_images_directory():
    os.makedirs(images_directory, exist_ok=True)
This function creates the directory for storing images if it doesn't exist.

Blockchain Initialization:

python
Copy code
def init_blockchain():
    # Global variable to store the Web3 instance
    global blockchain
    blockchain = Web3(Web3.EthereumTesterProvider())

    # Smart contract source code
    # (Simple image ownership contract with an 'uploadImage' function)
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

    # Compile the contract
    compiled_contract = blockchain.eth.compileSolidity(contract_source_code)
    contract_interface = compiled_contract['<stdin>:ImageOwnership']

    # Deploy the contract
    contract = blockchain.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    transaction_hash = contract.constructor().transact()
    transaction_receipt = blockchain.eth.waitForTransactionReceipt(transaction_hash)

    # Save the contract address for future interactions
    blockchain_contract_address = transaction_receipt['contractAddress']
    return blockchain_contract_address
This function initializes the Ethereum blockchain (using Ethereum Tester Provider for testing), compiles a simple smart contract for image ownership, deploys the contract, and returns the contract address.

Flask App Execution:

python
Copy code
if __name__ == '__main__':
    create_images_directory()

    # Initialize the blockchain and get the contract address
    contract_address = init_blockchain()

    app.run(port=5000)
This block checks if the script is the main module and then:

Creates the image directory.
Initializes the Ethereum blockchain and obtains the contract address.
Runs the Flask app on port 5000.
In summary, the script sets up a web application allowing users to upload images, view the uploaded images, and interacts with a basic Ethereum smart contract for image ownership. The smart contract is deployed on a local Ethereum blockchain for testing.
