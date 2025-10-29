from odoo import models, api
import random, time
from datetime import datetime, timedelta


class Dev(models.TransientModel):
    _name = "real_estate.dev"
    _description = "Used for development functionalities"

    config = {
        "properties" : 300,
        "buyers" : 12,
        "sellers" : 10,
        "offers_per_partner" : 5,
        "offer_price" : None, # None for random, Int for fixed
        "tags_to_create" : ["Modern", "New", "Renovated", "Luxurious", "Suburbs", "Centre", "By the sea", "Popular", "Limited time"],
        "property_types" : ["Flat", "House", "Cottage", "Duplex", "Terraced house", "Studio", "Villa"]
    }

    male_first_names = ["Liam", "Noah", "Oliver", "Elijah", "James", "William", "Benjamin", "Lucas", "Henry", "Alexander", "Ethan", "Michael", "Daniel", "Logan", "Jackson", "Sebastian", "Jack", "Owen", "Samuel", "Levi"]

    female_first_names = ["Rebecca", "Ann", "Susan", "Samantha", "Marianne", "Charlotte", "Ellen", "Emma", "Olivia", "Ava", "Sophia", "Isabella", "Mia", "Amelia", "Harper", "Evelyn", "Abigail", "Ella", "Charlotte", "Scarlett", "Grace", "Lily", "Chloe", "Aria", "Hannah", "Zoe", "Nora"]

    first_names = male_first_names + female_first_names
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]

    cities = ["London", "New York", "Hamburg", "Paris", "Berlin", "Madrid","Rome", "Amsterdam", "Lisbon", "Vienna", "Prague", "Budapest", "Warsaw",]
    orientations = ["north", "south", "east", "west"]

    adjectives = ["cosy", "renovated", "bright", "scenic", "exclusive", "spacious", "luxurious"]

    def seed(self):
        print("*****************************************************************************************************")
        print("SEEDING THE DATABASE")
        print("*****************************************************************************************************")

        self.env["real_estate.property_tag"].search([]).unlink()
        self.env["real_estate.offer"].search([]).unlink()
        self.env["real_estate.buyer"].search([]).unlink()
        self.env["real_estate.property_type"].search([]).unlink()
        self.prepare_properties_for_deletion()
        self.env["real_estate.property"].search([]).unlink()
        self.env["real_estate.seller"].search([]).unlink()
        ##TODO: What happens to property_tags junction table when these are unlinked/deleted ^?

        self.seed_buyers()
        self.seed_sellers()
        self.seed_tags()
        self.seed_types()
        self.seed_properties()
        self.seed_offers()

        self.sell_properties_and_reject_offers()

    def seed_buyers(self):

        print("SEEDING BUYERS - before group check")

        group_buyer = self.env.ref("real_estate.group_buyer", raise_if_not_found=False)
        if not group_buyer:
            raise ValueError("Group 'real_estate.group_buyer' not found. Make sure it exists")

        print("SEEDING BUYERS - after group check")

        for i in range(self.config["buyers"]):
            fname = random.choice(self.first_names)
            lname = random.choice(self.last_names)
            email = f"{fname}.{lname}.seller@test.com"

            partner = self.env["res.partner"].create({
                "name" : f"{fname} {lname}",
                "email" : email
            })

            user = self.env["res.users"].create({
                "partner_id" : partner.id,
                "login" : email,
                "groups_id": [(4, group_buyer.id)],
            })

            self.env["real_estate.buyer"].create({
                "user_id" : user.id
            })

    def seed_sellers(self):
        group_seller = self.env.ref("real_estate.group_seller", raise_if_not_found=False)
        if not group_seller:
            raise ValueError("Group 'real_estate.group_seller' not found. Make sure it exists")
                         
        for i in range(self.config["sellers"]):
            fname = random.choice(self.first_names)
            lname = random.choice(self.last_names)
            email = f"{fname}.{lname}.seller@test.com"

            partner = self.env["res.partner"].create({
                "name" : f"{fname} {lname}",
                "email" : email
            })

            user = self.env["res.users"].create({
                "partner_id" : partner.id,
                "login" : email,
                "groups_id": [(4, group_seller.id)],
            })

            self.env["real_estate.seller"].create({
                "user_id" : user.id
            })

    def prepare_properties_for_deletion(self):
        """ 
        There is a delete CRUD override in properies that prevents deletion if a property has status "offer_received" 
        We have to change the statuses of all properties before deleting them.
        """

        properties = self.env['real_estate.property'].search([])
        properties.status = 'new'

    def seed_offers(self):
        properties = self.env["real_estate.property"].search([])
        buyers = self.env["real_estate.buyer"].search([])

        print("BUYERS")
        print(buyers)

        for property in properties:
            if random.randint(1, 10) > 3: # Whether to create offers for this property or not
                number_of_offers = random.randint(1, 10)
                offer_values = []
                for i in range(number_of_offers):
                    price = self.config["offer_price"] if self.config["offer_price"] else property.expected_price * (random.randint(9, 13) / 10)
                    offer_values.append({
                        "status" : None,
                        "price" : price,
                        "buyer_id" : random.choice(buyers).id,
                        "property_id" : property.id,
                        "type_id" : property.property_type_id.id
                    })

                self.env["real_estate.offer"].create(offer_values)

    def seed_properties(self):
        property_values = []
        users = self.env["real_estate.seller"].search([])
        property_types = self.env["real_estate.property_type"].search([])
        all_tag_ids = self.env['real_estate.property_tag'].search([]).ids

        for i in range(self.config["properties"]):
            property_type = random.choice(property_types)
            city = random.choice(self.cities)
            garden = random.randint(0,1)
            garden_area = random.randint(100, 1000) if garden else 0
            garden_orientation = random.choice(self.orientations) if garden else None;
            random_tag_ids = random.sample(all_tag_ids, random.randint(1, 5))
            
            property_values.append({
                "name" : self.create_name(property_type.name, city),
                "property_type_id" : property_type.id,
                "description" : f"Lorem ipsum sit dollor amet. Lorem ipsum sit dollor amet. Lorem ipsum sit dollor amet. Lorem ipsum sit dollor amet. Lorem ipsum sit dollor amet. Lorem ipsum sit dollor amet. Lorem ipsum sit dollor amet. Lorem ipsum sit dollor amet. Lorem ipsum sit dollor amet. Lorem ipsum sit dollor amet. Lorem ipsum sit dollor amet. Lorem ipsum sit dollor amet.",
                "postcode" : 12345, ##TODO
                "date_availability" : datetime.now() + timedelta(days=random.randint(1, 20)),
                "expected_price" : random.randint(1, 100) * 10000,
                # "selling_price" : random.randint(1, 100) * 10000,
                "selling_price" : None,
                "bedrooms" : random.randint(1, 4),
                "living_area" : random.randint(50, 800),
                "facades" : random.randint(1, 4),
                "garage" : random.randint(0,1),
                "garden" : garden,
                "garden_area" : garden_area,
                "garden_orientation" : garden_orientation,
                "validity" : random.randint(1,20),
                "status" : "new",
                "seller_id" : random.choice(users).id,
                "buyer_id" : None,
                "tag_ids" : random_tag_ids
            })
        self.env["real_estate.property"].create(property_values)

    def seed_tags(self):
        tag_vals = []
        for tag in self.config["tags_to_create"]:
            tag_vals.append({
                "name" : tag
            })
        self.env["real_estate.property_tag"].create(tag_vals)

    def seed_types(self):
        type_values = []
        for type in self.config["property_types"]:
            type_values.append({
                "name" : type
            })
        self.env["real_estate.property_type"].create(type_values)
    
    def create_name(self, property_type: str, city: str):
        name = ""
        if random.randint(1, 10) > 2:
            # adjs = random.choices(self.adjectives, k=random.randint(1, 1))
            adj = random.choice(self.adjectives)
            name = adj.capitalize() + " "

        name += f"{property_type.lower()} in {city}" 
        name = name[0].upper() + name[1:]
        return name

    def sell_properties_and_reject_offers(self):
        properties = self.env["real_estate.property"].search([])
        for prop in properties:
            if prop.offer_ids:
                time.sleep(0.01)
                if random.randint(1,10) > 7:
                    # Sell the property
                    best_offer = max(prop.offer_ids, key=lambda offer: offer.price, default=False)
                    best_offer.action_accept()
                    prop.status = "sold"
                else:
                    # Reject some offers
                    for offer in prop.offer_ids:
                        if random.randint(1,3) == 3:
                            offer.action_refuse()
