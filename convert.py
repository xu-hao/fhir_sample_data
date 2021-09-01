import sys
import json
import os
import os.path

input_dir, output_dir = sys.argv[1:]

for filename in os.listdir(input_dir):
    print(f"loading {filename}")
    with open(os.path.join(input_dir, filename)) as f:
        bundle_obj = json.load(f)

    for entry_obj in bundle_obj["entry"]:
        resc_obj = entry_obj["resource"]
        resc_type = resc_obj["resourceType"]
        id = resc_obj["id"]
        if "subject" in resc_obj:
            resc_obj["subject"]["reference"] = resc_obj["subject"]["reference"].replace("urn:uuid:", "Patient/") 
        if "encounter" in resc_obj:
            resc_obj["encounter"]["reference"] = resc_obj["encounter"]["reference"].replace("urn:uuid:", "Encounter/")
        if resc_type == "Observation":
            resc_type = "Observation_Labs"
        if resc_type == "Procedure":
            resc_obj["performedDateTime"] = resc_obj["performedPeriod"]["start"]
        if resc_type == "MedicationRequest":
            resc_obj["start"] = resc_obj["authoredOn"]
        resc_dir = os.path.join(output_dir, resc_type)
        os.makedirs(resc_dir, exist_ok=True)
        print(f"writing {resc_dir} / {id}")
        with open(os.path.join(resc_dir, id), "w") as outf:
            json.dump({
                "resourceType": "Bundle",
                "entry": [{
                    "resource": resc_obj
                }]
            }, outf)
    

