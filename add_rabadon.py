import json

# Load index
with open('items/index.json', 'r') as f:
    index = json.load(f)

# Add Rabadon's Deathcap
index['items']["Rabadon's Deathcap"] = {
    'file': 'rabadons_deathcap.json',
    'category': 'legendary', 
    'cost': 3400,
    'tier': 'S'
}

index['total_items'] = len(index['items'])

# Save updated index
with open('items/index.json', 'w') as f:
    json.dump(index, f, indent=2)

print("Added Rabadon's Deathcap to index!")