# 1.1 Installation
# The first step is to download the Python client library for Azure Blob Storage. The below command can be used for installation.

# pip install azure-storage-blob
# 1.2 Creating a Container Client
# For accessing the blobs, we require the container client object or the blob client object. The connection string and the container name has to be provided to get the container client.

from azure.storage.blob import BlobServiceClient, BlobClient

def get_details():
 connection_string = 'DefaultEndpointsProtocol=https;AccountName=your_account_name;AccountKey=your_account_key'
 container_name = 'your_container_name'
 return connection_string, container_name

def get_clients_with_connection_string():
 connection_string, container_name = get_details()
 blob_service_client = BlobServiceClient.from_connection_string(connection_string)
 container_client = blob_service_client.get_container_client(container_name)
 return container_client
# 1.3 Read from blob with Connection String
# The following code snippet can be used to read the file from blob. After reading the file we can either write the byte contents to a file or we can store it in memory based on our use case.

def read_from_blob(blob_file_path):
 container_client = get_clients_with_connection_string()
 blob_client = container_client.get_blob_client(blob_file_path)
 byte_data= blob_client.download_blob().readall()
 return byte_data

def save_to_local_system(byte_file, filename):
 with open(f'{filename}', 'wb') as f:
 f.write(byte_file)
blob_file_path = "your_blob_file_path"
filename_in_local = "your_local_filename_for_saving"

byte_data = read_from_blob(blob_file_path)

# Optional
# save_to_local_system(byte_data, filename_in_local)
# 1.4 List the files in a folder using Connection String
# After getting the container client, by calling the list_blobs function we can list all the files in a particular folder.

def list_files_in_blob(folder_name):
 container_client = get_clients_with_connection_string()
 file_ls = [file['name'] for file in list(container_client.list_blobs(name_starts_with=folder_name))]
 return file_ls
folder_name = "your_folder_name"

file_ls = list_files_in_blob(folder_name)
# 1.5 Upload to blob storage using Connection String
# For uploading the file to the blob storage, we first have to read the file in our local system as bytes and then upload the byte information to the blob storage. The file will be uploaded to the blob and saved as the blob name provided. We get the blob client object by providing the connection string, container name and the blob name.

def read_from_local_system(local_filename):
 with open(f'{local_filename}', 'rb') as f:
 binary_content = f.read()
 return binary_content 

def upload_to_blob_with_connection_string(file_name,blob_name):
 connection_string, container_name = get_details()
 blob = BlobClient.from_connection_string(connection_string, container_name=container_name, blob_name=blob_name)
 with open(file_name, "rb") as data:
 blob.upload_blob(data)
local_filename = "your_local_filename"
blob_name = "your_blob_name"

byte_data = read_from_local_system(local_filename)
upload_to_blob_with_connection_string(file_name,blob_name)
# 1.6 Delete files with Connection String
# For Deleting a file in blob storage, we require the Blob client object. Based on our choice of deletion, we can send the parameters to the delete_blob function

# Delete just the blob.
# Delete just the snapshots.
# Delete the snapshots along with the blob.
# If the blob has any associated snapshots, you must delete all of its snapshots to delete the blob.
# The following example deletes a blob and its snapshots:

# To delete only the snapshots and not the blob itself, you can pass the parameter delete_snapshots="only".
# To delete just the blob we can call the functions without any parameters

def delete_blob(blob_name):
 connection_string, container_name = get_details()
 blob = BlobClient.from_connection_string(connection_string, container_name=container_name, blob_name=blob_name)
 blob.delete_blob(delete_snapshots="include")
 print(f"Deleted {blob_name}")

blob_name = "your_blob_name"

delete_blob(blob_name)