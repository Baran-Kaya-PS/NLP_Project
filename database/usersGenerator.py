import json
import random

# Generate random user data
def generate_random_user(user_id):
    first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia"]
    domains = ["example.com", "mail.com", "test.com", "demo.com", "sample.com"]

    name = random.choice(first_names) + " " + random.choice(last_names)
    email = name.lower().replace(" ", ".") + "@" + random.choice(domains)
    password = "password" + str(random.randint(100, 999))

    user = {
        "id": str(user_id),
        "nom": name,
        "email": email,
        "motDePasse": password,
        "historiqueRecherches": [],
        "evaluations": []
    }
    return user

# Generate a list of users
def generate_users(num_users):
    users = []
    for i in range(1, num_users + 1):
        users.append(generate_random_user(i))
    return users

# Save generated users to a JSON file
def save_users_to_json(users, file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)

# Main function
def main():
    num_users = 100  # Number of users to generate
    file_name = "generated_users.json"
    users = generate_users(num_users)
    save_users_to_json(users, file_name)
    print(f"Generated {num_users} users and saved to {file_name}")

if __name__ == "__main__":
    main()
