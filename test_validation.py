#!/usr/bin/env python3
"""
Test script to verify username and email validation works correctly
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netfix.settings')
django.setup()

from users.forms import CustomerSignUpForm, CompanySignUpForm

def test_customer_validation():
    print("Testing Customer Registration Validation...")
    
    # Test with existing username
    print("\n1. Testing duplicate username:")
    form_data = {
        'username': 'testuser',  # This already exists
        'email': 'newemail@example.com',
        'date_of_birth': '1990-01-01',
        'password1': 'newpassword123',
        'password2': 'newpassword123'
    }
    form = CustomerSignUpForm(data=form_data)
    if not form.is_valid():
        print(f"✅ Username validation works: {form.errors['username'][0]}")
    else:
        print("❌ Username validation failed - form should be invalid")
    
    # Test with existing email
    print("\n2. Testing duplicate email:")
    form_data = {
        'username': 'newuser',
        'email': 'test@example.com',  # This already exists
        'date_of_birth': '1990-01-01',
        'password1': 'newpassword123',
        'password2': 'newpassword123'
    }
    form = CustomerSignUpForm(data=form_data)
    if not form.is_valid():
        print(f"✅ Email validation works: {form.errors['email'][0]}")
    else:
        print("❌ Email validation failed - form should be invalid")
    
    # Test with both existing
    print("\n3. Testing both duplicate username and email:")
    form_data = {
        'username': 'testuser',  # This already exists
        'email': 'test@example.com',  # This already exists
        'date_of_birth': '1990-01-01',
        'password1': 'newpassword123',
        'password2': 'newpassword123'
    }
    form = CustomerSignUpForm(data=form_data)
    if not form.is_valid():
        print(f"✅ Both validations work:")
        if 'username' in form.errors:
            print(f"   Username: {form.errors['username'][0]}")
        if 'email' in form.errors:
            print(f"   Email: {form.errors['email'][0]}")
    else:
        print("❌ Validation failed - form should be invalid")
    
    # Test with unique values
    print("\n4. Testing unique username and email:")
    form_data = {
        'username': 'uniqueuser',
        'email': 'unique@example.com',
        'date_of_birth': '1990-01-01',
        'password1': 'newpassword123',
        'password2': 'newpassword123'
    }
    form = CustomerSignUpForm(data=form_data)
    if form.is_valid():
        print("✅ Unique values validation works - form is valid")
    else:
        print(f"❌ Unique values failed: {form.errors}")

def test_company_validation():
    print("\n\nTesting Company Registration Validation...")
    
    # Test with existing username
    print("\n1. Testing duplicate username:")
    form_data = {
        'username': 'testuser',  # This already exists
        'email': 'company@example.com',
        'field_of_work': 'Plumbing',
        'password1': 'newpassword123',
        'password2': 'newpassword123'
    }
    form = CompanySignUpForm(data=form_data)
    if not form.is_valid():
        print(f"✅ Username validation works: {form.errors['username'][0]}")
    else:
        print("❌ Username validation failed - form should be invalid")
    
    # Test with existing email
    print("\n2. Testing duplicate email:")
    form_data = {
        'username': 'companyuser',
        'email': 'test@example.com',  # This already exists
        'field_of_work': 'Plumbing',
        'password1': 'newpassword123',
        'password2': 'newpassword123'
    }
    form = CompanySignUpForm(data=form_data)
    if not form.is_valid():
        print(f"✅ Email validation works: {form.errors['email'][0]}")
    else:
        print("❌ Email validation failed - form should be invalid")

if __name__ == "__main__":
    test_customer_validation()
    test_company_validation()
    print("\n🎉 Validation testing complete!")
