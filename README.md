# Cross-Account Billing Read-Only Access (AWS)

This guide explains how to allow **Account A** to view **Billing
(read-only)** of **Account B** using AssumeRole and CloudFormation.

------------------------------------------------------------------------

## Architecture Flow

Login → Account A → Switch Role → Account B → Billing (Read Only)

------------------------------------------------------------------------

## Steps in Account B

1.  Login to Account B\
2.  Enable IAM billing access\
3.  Open CloudFormation\
4.  Upload template\
5.  Enter Account A ID\
6.  Create stack

------------------------------------------------------------------------

## Steps in Account A

1.  Login\
2.  Switch role\
3.  Enter Account B ID\
4.  Role: BillingReadOnlyClient\
5.  Open billing

------------------------------------------------------------------------

## CloudFormation Template

\`\`\`yaml AWSTemplateFormatVersion: "2010-09-09" Description: Allow
Account A to view billing

Parameters: AccountAId: Type: String Description: Account ID that will
access this account

Resources: BillingReadOnlyRole: Type: AWS::IAM::Role Properties:
RoleName: BillingReadOnlyClient

      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub "arn:aws:iam::${AccountAId}:root"
            Action: sts:AssumeRole

      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/job-function/Billing
