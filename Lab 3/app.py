from ariadne import ObjectType, graphql_sync, make_executable_schema, load_schema_from_path
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify

from api import resolver

type_defs = load_schema_from_path('schema.graphql')

student = ObjectType('Student')
classes = ObjectType('Class')
query = ObjectType('Query')
mutation = ObjectType('Mutation')

query.set_field('classes', resolver.classes)
query.set_field('students', resolver.students)
query.set_field('all_classes', resolver.all_classes)
query.set_field('student', resolver.student)

mutation.set_field('create_student', resolver.create_student)
mutation.set_field('create_class', resolver.create_class)
mutation.set_field('add_student_to_class', resolver.add_student_to_class)

schema = make_executable_schema(type_defs, [classes, student, query, mutation])

app = Flask(__name__)

@app.route("/", methods=["POST"])
def server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

@app.route("/", methods=["GET"])
def playground():
    return PLAYGROUND_HTML, 200


if __name__ == "__main__":
    app.run(debug=True)
