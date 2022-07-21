import aws_cdk as core
import aws_cdk.assertions as assertions

from ec2.ec2_stack import Ec2Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in ec2/ec2_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Ec2Stack(app, "ec2")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
