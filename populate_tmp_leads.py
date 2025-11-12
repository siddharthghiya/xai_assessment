from database import insert_lead

leads_data = [
    ("Alice Johnson", "Tech Innovations Inc.", "alice.j@techmail.com", "Experienced software developer seeking new opportunities in AI and machine learning.", "Female", 28, "Software Developer", "IT", "Medium", "New York, USA", "Email"),
    ("Bob Smith", "Green Acres Farm", "bob.smith@farmnet.org", "Seasoned farmer looking to modernize operations with sustainable tech solutions.", "Male", 45, "Farmer", "Agriculture", "Low", "Iowa, USA", "Phone"),
    ("Carla Rodriguez", "ArtWorld Gallery", "carla.r@artworld.com", "Talented artist interested in digital art collaborations and exhibitions.", "Female", 32, "Artist", None, "Low", "Paris, France", "Email"),
    ("David Lee", "University of London", "david.lee@uni.edu", "Computer science student eager for internships in web development and data science.", "Male", 21, "Student", None, None, "London, UK", "SMS"),
    ("Elena Martinez", "HealthCare Network", "elena.m@healthcare.net", "Dedicated nurse exploring telemedicine and health tech opportunities.", "Female", 55, "Nurse", "Healthcare", "Medium", "Madrid, Spain", "Phone"),
    ("Frank Wilson", "Retired Professionals Assoc.", "frank.w@retiredlife.com", "Retiree with extensive business experience looking for consulting gigs.", "Male", 68, "Retiree", None, "Medium", "Florida, USA", "Email"),
    ("Grace Kim", "FinanceHub Corp", "grace.k@financehub.com", "Certified accountant specializing in fintech audits and compliance.", "Female", 40, "Accountant", "Finance", "High", "Seoul, South Korea", "Email"),
    ("Henry Patel", "BuildRight Construction", "henry.p@constructionco.com", "Skilled builder interested in sustainable and green building projects.", "Male", 37, "Builder", "Construction", "Medium", "Mumbai, India", "Phone"),
    ("Isabella Chen", "Music Production Studios", "isabella.c@musicprod.net", "Rising musician seeking production partnerships and label deals.", "Female", 26, "Musician", "Entertainment", "Low", "Los Angeles, USA", "SMS"),
    ("Jack Thompson", "Legal Eagles Firm", "jack.t@legal.com", "Experienced lawyer focusing on corporate and tech law.", "Male", 50, "Lawyer", "Legal", "High", "Sydney, Australia", "Email"),
    ("Kira Nguyen", "EduTech Org", "kira.n@edutech.org", "Passionate teacher interested in edtech tools and online learning platforms.", "Female", 29, "Teacher", "Education", "Medium", "Hanoi, Vietnam", "Email"),
    ("Liam Garcia", "Startup.io", "liam.g@startup.io", "Entrepreneur building innovative tech startups in e-commerce.", "Male", 31, "Entrepreneur", "Tech Startup", "Medium", "Berlin, Germany", "Email"),
    ("Mia Lopez", "Wellness Center", "mia.l@wellnesscenter.com", "Certified yoga instructor offering wellness and mindfulness programs.", "Female", 42, "Yoga Instructor", "Wellness", "Low", "Bali, Indonesia", "Phone"),
    ("Noah Anderson", "Engineering Firm", "noah.a@engineeringfirm.com", "Mechanical engineer specializing in manufacturing automation.", "Male", 38, "Engineer", "Manufacturing", "High", "Tokyo, Japan", "Email"),
    ("Olivia Brown", "Nonprofit Org", "olivia.b@nonprofit.org", "Dedicated activist working on environmental and social justice causes.", "Female", 34, "Activist", "Nonprofit", "Low", "Nairobi, Kenya", "SMS"),
    ("Pablo Ramirez", "FoodService Co", "pablo.r@foodservice.com", "Creative chef passionate about fusion cuisine and hospitality.", "Male", 27, "Chef", "Hospitality", "Medium", "Mexico City, Mexico", "Phone"),
    ("Quinn Taylor", "Fashion Design Studio", "quinn.t@fashiondesign.com", "Innovative designer focusing on sustainable fashion.", "Other", 24, "Designer", "Fashion", "Low", "Milan, Italy", "Email"),
    ("Riley White", "Real Estate Pro", "riley.w@realestatepro.com", "Expert real estate agent specializing in commercial properties.", "Female", 46, "Real Estate Agent", "Real Estate", "High", "Toronto, Canada", "Phone"),
    ("Sam Kim", "Travel Agency Net", "sam.k@travelagency.net", "Travel agent curating unique adventure and cultural tours.", "Male", 33, "Travel Agent", "Tourism", "Medium", "Bangkok, Thailand", "Email"),
    ("Tara Singh", "Fitness Coach Services", "tara.s@fitnesscoach.com", "Professional fitness coach offering personalized training programs.", "Female", 39, "Fitness Coach", "Health & Fitness", "Medium", "Dubai, UAE", "SMS"),
]

for name, company, email, description, gender, age, profession, industry, income_level, location, preferred_contact in leads_data:
    insert_lead(name, email, company=company, description=description, gender=gender, age=age, profession=profession, industry=industry, income_level=income_level, location=location, preferred_contact=preferred_contact)

print("Inserted 20 new leads into the database.")
