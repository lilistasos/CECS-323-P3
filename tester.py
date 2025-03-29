from pymongo import MongoClient

def connect():
    connection_string = "mongodb://localhost:27017"
    client = MongoClient(connection_string)
    return client['project3']


if __name__ == "__main__":
    db = connect()

    print("Project 3:")
    problem = input("Would you like to do problem 1 or 2: ")

    if problem == '1':
        name = input("Input Name: ")

        pipeline = [
            {"$match": {"name": name}},
            {"$unwind": "$ownedSets"},
            {"$lookup": {"from": "inventories", "localField": "ownedSets.inventoryId", "foreignField": "_id",
                         "as": "inventory"}},
            {"$unwind": "$inventory"},
            {"$unwind": "$inventory.parts"},
            {"$group": {
                "_id": {"partName": "$inventory.parts.part.partName", "colorName": "$inventory.parts.color.colorName"},
                "totalQuantity": {"$sum": "$inventory.parts.quantity"}
            }},
            {"$project": {
                "_id": 0,
                "partName": "$_id.partName",
                "colorName": "$_id.colorName",
                "totalQuantity": 1
            }},
            {"$sort": {"partName": 1, "colorName": 1}}
        ]

        results = db["users"].aggregate(pipeline)

        for result in results:
            print(
                f"Quantity: {result['totalQuantity']}, "
                f"Part Name: {result['partName']}, "
                f"Color Name: {result['colorName']}"
            )

    elif problem == '2':
        setNumber = input("Enter the set number: ")
        versionNumber = int(input("Enter the version number: "))

        pipeline = [
            {"$match": {"setNumber": setNumber, "version": versionNumber}},
            {"$unwind": "$parts"},
            {"$match": {"parts.isSpare": False}},
            {"$project": {
                "_id": 0,
                "quantity": "$parts.quantity",
                "partName": "$parts.part.partName",
                "colorName": "$parts.color.colorName"
            }},
            {"$sort": {"partName": 1, "colorName": 1}}
        ]

        results = db["inventories"].aggregate(pipeline)

        for result in list(results):
            print(
                f"Quantity: {result['quantity']},"
                f" Part Name: {result['partName']}, "
                f"Color Name: {result['colorName']}"
            )

    else:
        print("Invalid selection. Please enter 1 or 2.")
