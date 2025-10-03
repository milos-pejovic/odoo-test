from odoo import models, api
import random
from datetime import datetime, timedelta


class Dev(models.TransientModel):
    _name = "real_estate.dev"
    _description = "Used for development functionalities"

    seeding_data = {
        "properties" : 100,
        "partners" : 10,
        "offers_per_partner" : 5,
        "tags_to_create" : ["Modern", "New", "Renovated", "Luxurious", "Suburbs", "Centre", "By the sea", "Popular", "Limited time"],
        "property_types" : ["Flat", "House", "Cottage", "Duplex"]
    }

    first_names = ["James", "Sam", "John", "Ian", "Ann", "Peter", "Susan", "Liam", "Gunnar"]
    last_names  = ["Johnson", "Samson", "Connor", "Peterson", "Li", "Gunnarson"]
    cities = ["London", "New York", "Hamburg", "Paris", "Berlin", "Madrid","Rome", "Amsterdam", "Lisbon", "Vienna", "Prague", "Budapest", "Warsaw",]
    orientations = ["north", "south", "east", "west"]

    def seed(self):
        print("SEEDING THE DATABASE")

        self.env["real_estate.property_tag"].search([]).unlink()
        self.env["real_estate.offer"].search([]).unlink()
        self.env["real_estate.partner"].search([]).unlink()
        self.env["real_estate.property_type"].search([]).unlink()
        self.prepare_properties_for_deletion()
        self.env["real_estate.property"].search([]).unlink()
        ##TODO: What happens to property_tags junction table when these are unlinked/deleted ^?

        self.seed_partners()
        self.seed_tags()
        self.seed_types()
        self.seed_properties()
        self.seed_offers()

    def prepare_properties_for_deletion(self):
        """ 
        There is a delete CRUD override in  properies that prevents deletion if a propert has status "offer_received" 
        We have to change the statuses of all proeprties before deleting them.
        """

        properties = self.env['real_estate.property'].search([])
        properties.status = 'new'

    def seed_offers(self):
        properties = self.env["real_estate.property"].search([])
        partners = self.env["real_estate.partner"].search([])

        for property in properties:
            if random.randint(1, 10) > 3: # Whether to create offers for this property or not
                number_of_offers = random.randint(1, 10)
                offer_values = []
                for i in range(number_of_offers):
                    offer_values.append({
                        "status" : None,
                        "price" : property.expected_price * (random.randint(7, 13) / 10),
                        "partner_id" : random.choice(partners).id,
                        "property_id" : property.id,
                        "type_id" : property.property_type_id.id
                    })

                self.env["real_estate.offer"].create(offer_values)

    def seed_properties(self):
        property_values = []
        users = self.env["res.users"].search([])
        property_types = self.env["real_estate.property_type"].search([])
        all_tag_ids = self.env['real_estate.property_tag'].search([]).ids

        for i in range(self.seeding_data["properties"]):
            property_type = random.choice(property_types)
            city = random.choice(self.cities)
            name = f"{property_type.name} in {city}"
            garden = random.randint(0,1)
            garden_area = random.randint(100, 1000) if garden else 0
            garden_orientation = random.choice(self.orientations) if garden else None;
            num_tags = random.randint(1, len(all_tag_ids))
            random_tag_ids = random.sample(all_tag_ids, min(num_tags, len(all_tag_ids)))
            
            property_values.append({
                "name" : name,
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

    def seed_partners(self):       
        properties_vals = []
        for i in range(self.seeding_data["partners"]):
            fname = random.choice(self.first_names)
            lname = random.choice(self.last_names)
            properties_vals.append(
                {"name" : f"{fname} {lname}"}
            )
        self.env["real_estate.partner"].create(properties_vals)

    def seed_tags(self):
        tag_vals = []
        for tag in self.seeding_data["tags_to_create"]:
            tag_vals.append({
                "name" : tag
            })
        self.env["real_estate.property_tag"].create(tag_vals)

    def seed_types(self):
        type_values = []
        for type in self.seeding_data["property_types"]:
            type_values.append({
                "name" : type
            })
        self.env["real_estate.property_type"].create(type_values)
    