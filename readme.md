# Update EC2 Security Groups using dynamic DNS IP

Simple Lambda funtion to update a Security Group using a DDNS IP. Useful if you need to update your security group(s) often because of clients using dynamic IPs being used to access your instance.

## IAM Policy

This is the policy that grants the permissions to modify EC2 security groups and write logs, register it in IAM and create / apply to the role used to execute the function:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeSecurityGroups",
        "ec2:AuthorizeSecurityGroupIngress",
        "ec2:RevokeSecurityGroupIngress"
      ],
      "Resource": "*"
    }
  ]
}
```

## Usage

Tag the rules of the security group using the description **DDNS_Update**.
Modify the script to use the appropriate **dynamic domain** and **security group id**.

## Authors

- **MacK** - _Initial work_ - [Oddbytes](https://oddbytes.net)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Lambda function inspired by Grig Gheorghiu's [Modifying EC2 security groups via AWS Lambda functions](https://medium.com/@griggheo/modifying-ec2-security-groups-via-aws-lambda-functions-115a1828cdb6) post in [Medium](https://medium.com) and modified slightly.

Made with ❤️ by Oddbytes.
