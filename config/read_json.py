import json



def read_json(json_file):
    # Load algorithm configuration from JSON file
    with open(json_file, "r") as config_file:
        config = json.load(config_file)

    # Select ECG record defined in the configuration
    record_name = config["record"]

    print("\n===================================")
    print("ECG Measurement Algorithm")
    print("Record:", record_name)
    print("===================================")

    return config