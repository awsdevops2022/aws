import aws_cdk as core
import aws_cdk.assertions as assertions

from batch.batch_stack import BatchStack

# example tests. To run these tests, uncomment this file along with the example
# resource in batch/batch_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = BatchStack(app, "batch")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
