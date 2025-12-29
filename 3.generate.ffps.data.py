from faker import Faker
import pandas as pd
import mysql.connector
import random
from datetime import datetime, timedelta

# locales to generate names from different countries
locale_list = ['en_US', 'it_IT', 'en_GB','da_DK', 'en_AU', 'en_CA', 'en_IN', 'en_PH', 'fr_FR', 'es_ES', 'es_MX', 'nl_NL', 'pl_PL']

fake = Faker(locale_list)

# count of ffps to be generated
real_ffps = 10000
fake_ffps = 1000

# main fun to generate ffps data
def ffps_date(real_ffps, fake_ffps):
    
    members_list = []
    details_list = []
    enrolment_list = []
    claims_list = []
    transactions_list = []
    tier_list = []
    cs_contact_list = []
    
    # generate real ffps first
    for i in range(real_ffps):
        ffn = '5000' + ''.join(fake.random_elements(elements='1234567890', length=8))
        first_name = fake.first_name()
        last_name = fake.last_name()
        enroll_date = fake.date_time_between(start_date='-3y', end_date='now') # real ffps joined over the past 3 year till now
        country = fake.country_code().upper() # member country & to use for passport initials
        
        members_list.append({
            'ffp_number' : ffn,
            'first_name' : first_name,
            'last_name' : last_name,
            'birth_date' : fake.date_of_birth(minimum_age=18, maximum_age= 80).isoformat(),
            'nationality' : country,
            'passport_number' : country + fake.bothify(text='#######'), #XX01234567
            'verified' : 1
        })
        
        details_list.append({
            'ffp_number' : ffn,
            'email' : f"{first_name.lower()}.{last_name.lower()}{random.randint(1,9999)}@{fake.free_email_domain()}", # real ffps mostly use real first & last name email ids
            'phone_number' : fake.phone_number(),
            'country' : country,
            'enrollment_date' : enroll_date
        })
        
        enrolment_list.append({
            'ffp_number' : ffn,
            'enrolment_date' : enroll_date,
            'enrolment_ip' : fake.ipv4(),
            'device' : fake.user_agent(), # device used to enroll
            'channel' : 'Web',
            'status' : 'Active'
        })
        
        tier_list.append({
            'ffp_number' : ffn,
            'tier_level' : random.choices(['Bronze', 'Silver', 'Gold', 'Platinum', 'Emerald'], weights=[90, 80, 50, 40, 20])[0],
            'status' : 'Active',
            'start_date' : enroll_date.date(),
            'end_date' : (enroll_date + timedelta(days= 800)).date(),
            'qualification_method' : 'Miles accrual'
        })
        
        # assuming about 20% of real members claim their miles
        if random.random() < 0.20:
            miles_earned = random.choice([500, 900, 1200, 2500, 5000, 8000])
            
        # their accrual date is 30 to 120 days after enrollment date
            earn_date = enroll_date + timedelta(days=random.randint(30, 120))
            transactions_list.append({
                'ffp_number' : ffn,
                'type' : 'Accrual',
                'transaction_date' : earn_date,
                'processing_date' : earn_date,
                'status' : 'Accepted',
                'source' : random.choice(['Web', 'Partner', 'Flight']),
                'miles_amount' : miles_earned
            })
        
        # assuming about 30% of real members who accrual their miles actually redeem them
            if random.random() < 0.30:
            
            # their redeem date is 30 to 60 days after their accrual date
                    redeem_date = earn_date + timedelta(days=random.randint(30, 120))
                    transactions_list.append({
                        'ffp_number' : ffn,
                        'type' : random.choice(['One-way flight', 'Flight upgrade', 'Reward shop']),
                        'transaction_date' : redeem_date,
                        'processing_date' : redeem_date,
                        'status' : 'Accepted',
                        'source' : 'Web',
                        'miles_amount' : -random.choice([500, 900, 1200, 2500, 5000]) # miles are spent in random amounts from 500 to 5000
                    })
    
    #fake ffps login devices
    fraud_device = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/118.0.0.0 Safari/537.36"
    
    # generate fake ffps
    for i in range(fake_ffps):
        ffn = '5000' + ''.join(fake.random_elements(elements='0123456789', length=8))
        
        # newly joined fake ffps in the past 7 days
        enroll_date = fake.date_time_between(start_date='-7d', end_date='now')
        first_name = fake.first_name()
        last_name = fake.last_name()
        fake_ffp_country = random.choice(['CN', 'RU','TR', 'US'])
        fake_ffp_email = fake.lexify(text='????????').lower() + str(random.randint(100,9999))
        
        # incorrect details on the ffp account but not identical
        members_list.append({
            'ffp_number' : ffn,
            'first_name' : first_name,
            'last_name'  : last_name,
            'birth_date' : random.choice(['1900-01-01', '1910-01-01', '1920-01-01', '1930-01-01']),
            'nationality' : fake_ffp_country,
            'passport_number' : fake_ffp_country + (fake.bothify(text='#######')),
            'verified' : 0
        })
        
        details_list.append({
            'ffp_number' : ffn,
        
        # fake ffps using the same email formats (xxxxxxxx1234@gmail.com)
            'email' : f'{fake_ffp_email}@user-verify.net', 
            'phone_number' : fake.phone_number(),
            'country' : fake_ffp_country,
            'enrollment_date' : enroll_date
        })
        
        # fake ffps using rotating different IP addresses
        enrolment_list.append({
            'ffp_number' : ffn,
            'enrolment_date' : enroll_date,
            'enrolment_ip' : fake.ipv4(),
            'device' : fraud_device, # but using the same device
            'channel' : 'Web',
            'status' : 'Active'
        })
        
        tier_list.append({
            'ffp_number': ffn,
            'tier_level' : 'Basic',
            'status' : 'Active',
            'start_date' : enroll_date.date(),
            'end_date' : (enroll_date + timedelta(days=700)).date(),
            'qualification_method' : 'Miles accrual'
        })
        
        # miles claim transactions equals miles redemptions
        
        current_balance = 0
        
        # claim 1-3 flights to accumlate balance before redemption
        num_claims = random.randint(1, 3)
        
        for _ in range(num_claims):
            
        # miles claimed in random amounts from past flights
            flight_miles = random.choice([4500, 8000, 12500, 22000])
            
        # retro claims for flights taking place 1-4 months earlier from enrollment
            flight_date = (enroll_date - timedelta(days=random.randint(30, 120))).date()
        
        # records of retro claims for past flights
            claims_list.append({
                'ffp_number': ffn,
                'date_submitted' : enroll_date, 
                'ticket_number' : '607' + fake.numerify(text='##########'),
                'flight_number' : 'EY' + fake.numerify(text='###'),
                'departure_date' : flight_date,
                'status' : 'Accepted'
            })
            
        # regestering the same amount of miles claimed in transactions table
            transactions_list.append({
                'ffp_number' : ffn,
                'type' : 'Accrual',
                'transaction_date' : enroll_date,
                'processing_date' : enroll_date,
                'status' : 'Accepted',
                'miles_amount' : flight_miles
            })
            
            current_balance += flight_miles
            
        # redeeming miles within 12-48 hours after accrual
        redemption_time = enroll_date + timedelta(hours=random.randint(12,48))
        
        # matching the amount of redeemed miles to the amount accrued
        if current_balance > 0:
            
            if random.random() < 0.60: # about 60% of the flights redeemed as oneway flight
                redemption_type = 'One-way flight'
            else:
                redemption_type = 'Reward shop' # 40% of the flights redeemed via reward shop
        
        # register redeemed flights & minus the current balance of miles
            transactions_list.append({
                'ffp_number' : ffn,
                'type' : redemption_type,
                'transaction_date' : redemption_time,
                'processing_date' : redemption_time,
                'status' : 'Accepted',
                'source' : 'Web',
                'miles_amount': -current_balance
            })
            
        # few members (about 5%) who contacted Customer Service claiming they did not authorize the redemption
        if random.random() < 0.05:
            cs_contact_list.append({
                'ffp_number' : ffn,
                'contact_time' : redemption_time + timedelta(hours=random.randint(1, 24)), # contact in the 24 hours after redemption
                'reason' : 'Unauthorized redemption',
                'channel' : random.choice(['Call', 'Email', 'Chat']),
                'case_status' : random.choice(['Open', 'In review', 'Closed'])
                })

    return (
        pd.DataFrame(members_list),
        pd.DataFrame(details_list),
        pd.DataFrame(enrolment_list),
        pd.DataFrame(claims_list),
        pd.DataFrame(transactions_list),
        pd.DataFrame(tier_list),
        pd.DataFrame(cs_contact_list))

conn = mysql.connector.connect(
    host = 'mac.local',
    user = 'root',
    password = 'password',
    database = 'abc'
)

cursor = conn.cursor()

# generate dataframes
members_df, details_df, enrolment_df, claims_df, transactions_df, tier_df, cs_df = ffps_date(real_ffps, fake_ffps)

# 1) members
cursor.executemany("""
INSERT INTO members (ffp_number, first_name, last_name, birth_date, nationality, passport_number, verified)
VALUES (%s,%s,%s,%s,%s,%s,%s)
""", members_df[['ffp_number','first_name','last_name','birth_date','nationality','passport_number','verified']].values.tolist())

# 2) member_details
cursor.executemany("""
INSERT INTO member_details (ffp_number, email, phone_number, country, enrollment_date)
VALUES (%s,%s,%s,%s,%s)
""", details_df[['ffp_number','email','phone_number','country','enrollment_date']].values.tolist())

# 3) enrolment
cursor.executemany("""
INSERT INTO enrolment (ffp_number, enrolment_date, enrolment_ip, device, channel, status)
VALUES (%s,%s,%s,%s,%s,%s)
""", enrolment_df[['ffp_number','enrolment_date','enrolment_ip','device','channel','status']].values.tolist())

# 4) tier
cursor.executemany("""
INSERT INTO tier (ffp_number, tier_level, status, start_date, end_date, qualification_method)
VALUES (%s,%s,%s,%s,%s,%s)
""", tier_df[['ffp_number','tier_level','status','start_date','end_date','qualification_method']].values.tolist())

# 5) claims
cursor.executemany("""
INSERT INTO claims (ffp_number, date_submitted, ticket_number, flight_number, departure_date, status)
VALUES (%s,%s,%s,%s,%s,%s)
""", claims_df[['ffp_number','date_submitted','ticket_number','flight_number','departure_date','status']].values.tolist())

# 6) transactions
cursor.executemany("""
INSERT INTO transactions (ffp_number, type, transaction_date, processing_date, status, source, miles_amount)
VALUES (%s,%s,%s,%s,%s,%s,%s)
""", transactions_df[['ffp_number','type','transaction_date','processing_date','status','source','miles_amount']].values.tolist())

# 7) cs_contacts
cursor.executemany("""
INSERT INTO cs_contacts (ffp_number, contact_time, reason, channel, case_status)
VALUES (%s,%s,%s,%s,%s)
""", cs_df[['ffp_number','contact_time','reason','channel','case_status']].values.tolist())

conn.commit()
cursor.close()
conn.close()
