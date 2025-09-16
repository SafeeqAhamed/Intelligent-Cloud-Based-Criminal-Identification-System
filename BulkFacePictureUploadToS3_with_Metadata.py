import boto3     # is a AWS SDK for Python – connects Python program to AWS services/resources

# Connect to S3
s3 = boto3.resource('s3')

# Get list of objects for indexing
# Each entry: (image filename, full name, crime type, wanted status)
images = [
    ('1.jpg',  'John Doe',        'Robbery',      'Wanted'),              #A list of tuples.---(image file name, person name)
    ('2.jpg',  'Jane Smith',      'Fraud',        'Not Wanted'),          #images[0]=filename
    ('3.jpg',  'David Beckham',   'Match Fixing', 'Wanted'),              #images[1]=person name
    ('4.png',  'Albert Einstein', 'No Crime',     'Not Wanted'),
    ('5.jpg',  'Isaac Newton',    'No Crime',     'Not Wanted'),
    ('6.png',  'Lionel Messi',    'Tax Evasion',  'Wanted'),
    ('7.jpeg', 'Nikola Tesla',    'No Crime',     'Not Wanted'),
    ('8.jpeg', 'MS Dhoni',        'No Crime',     'Not Wanted'),
    ('9.jpeg', 'Mithali Raj',     'No Crime',     'Not Wanted'),
    ('10.jpeg','Smriti Mandhana', 'No Crime',     'Not Wanted'),
    ('11.jpeg','Hardik Pandya',   'Match Fixing', 'Not Wanted'),
    ('12.jpeg','Yuvraj Singh',    'No Crime',     'Not Wanted'),
    ('13.jpg', 'Sachin Tendulkar','No Crime',     'Not Wanted'),
    ('14.jpeg','Yuzvendra Chahal','No Crime',     'Not Wanted'),
    ('15.jpeg','Virat Kohli',     'No Crime',     'Not Wanted'),
    ('16.jpg', 'Sunil Gavaskar',  'No Crime',     'Not Wanted'),
    ('17.jpg', 'Kapil Dev',       'No Crime',     'Not Wanted'),
    ('18.jpeg','Ruturaj Gaikwad', 'No Crime',     'Not Wanted'),
    ('19.jpeg','Kiran Kumar',     'Theft',        'Wanted'),
    ('20.jpeg','Vijay',           'Smuggling',    'Wanted'),
    ('21.jpeg','Shahrukh Khan',   'No Crime',     'Not Wanted'),
    ('22.jpg', 'Harleen Deol',    'No Crime',     'Not Wanted')
]

# Iterate through list to upload objects to S3   
for arr in images: 
    image = open(arr[0], 'rb')   # Open each image in read-binary mode 
                                  #Look for a image named 1.jpg in the current working directory
    
    #object to point location where we want to store the image in S3 bucket-->to Upload each image to bucket "criminal-images-bucket" inside folder "criminals/"
    object = s3.Object('criminal-images-bucket', 'criminals/' + arr[0])       

    # Upload with metadata (FullName, CrimeType, WantedStatus)
     #we can call (get,put,delete) methods on this object
    ret = object.put(
                   Body=image,                  
                   Metadata={            #extra info 
                            'fullname': arr[1],
                            'crime': arr[2],
                            'status': arr[3]
                            }
                   )
    #in return we get 'HTTPStatusCode': 200
    print(f"Uploaded {arr[0]} with metadata -> Name: {arr[1]}, Crime: {arr[2]}, Status: {arr[3]}")