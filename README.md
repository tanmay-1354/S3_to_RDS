# **📘 Cross-Account Billing Read-Only Access (AWS)**

This guide explains how to allow **Account A** to view **Billing (read-only)** of **Account B** using **AssumeRole \+ CloudFormation**.

No IAM user is created in Account B. Access is done securely using role switching.

---

## **🧭 Use Case**

You have full access to **Account A** and need billing read-only access to a client account (**Account B**).

---

## **🏗️ Architecture Flow**

Login  
   ↓  
Account A (Main Account)  
   ↓  
Switch Role  
   ↓  
Account B (Client Account)  
   ↓  
Open Billing (Read Only)

---

## **📍 Where to Deploy**

The CloudFormation template must be deployed in:

**Account B (Client Account)**

---

## **🔐 Permissions Required**

### **Account A**

* Admin/root access  
  **OR**  
* IAM user/role with `sts:AssumeRole` permission

### **Account B**

* Admin/root access to deploy CloudFormation  
* IAM access to Billing must be enabled

---

## **🚀 Setup Steps**

### **🟦 Steps in Account B (Client)**

#### **1️⃣ Login to Account B**

#### **2️⃣ Enable IAM Billing Access**

Go to:

**Billing → Account settings → Enable IAM access to billing**

---

#### **3️⃣ Open CloudFormation**

Create a new stack and upload the template file.

---

#### **4️⃣ Upload Template**

Template file name:

billing-cross-account.yaml

---

#### **5️⃣ Enter Parameter**

During stack creation you will be asked for:

AccountAId

Enter:

**AWS Account ID of Account A (source account)**

---

#### **6️⃣ Create Stack**

Wait until status shows:

CREATE\_COMPLETE

This will create a role:

BillingReadOnlyClient

---

### **🟩 Steps in Account A**

#### **7️⃣ Login to Account A**

#### **8️⃣ Click "Switch Role"**

Top right corner → Account → **Switch Role**

---

#### **9️⃣ Enter Details**

| Field | Value |
| ----- | ----- |
| Account ID | Account B ID |
| Role Name | BillingReadOnlyClient |
| Display Name | (optional) Billing-Client |

---

#### **🔟 Access Billing**

After switching role:

**Billing Console → View (Read-Only)**

---

## **📄 CloudFormation Template**

Save this as:

billing-cross-account.yaml

AWSTemplateFormatVersion: "2010-09-09"  
Description: Allow Account A to view billing

Parameters:  
  AccountAId:  
    Type: String  
    Description: Account ID that will access this account

Resources:  
  BillingReadOnlyRole:  
    Type: AWS::IAM::Role  
    Properties:  
      RoleName: BillingReadOnlyClient

      AssumeRolePolicyDocument:  
        Version: "2012-10-17"  
        Statement:  
          \- Effect: Allow  
            Principal:  
              AWS: \!Sub "arn:aws:iam::${AccountAId}:root"  
            Action: sts:AssumeRole

      ManagedPolicyArns:  
        \- arn:aws:iam::aws:policy/job-function/Billing

---

## **🧪 Test**

1. Deploy stack in **Account B**  
2. Switch role from **Account A**  
3. Open **Billing**

You should see **read-only billing access**.

---

## **🛡️ Security Notes**

* No IAM users created in client account  
* Only AssumeRole access  
* Billing read-only permissions only  
* Safe for production client environments

---

## **🏁 Done**

You now have secure cross-account billing visibility.

