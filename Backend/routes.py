from flask import request, jsonify

from app import app, db

from models import LessonPlan

from schemas import LessonPlanSchema

schema = LessonPlanSchema()

# CREATE
@app.route('/plans', methods=['POST'])
def create_plan():

    data = request.json

    errors = schema.validate(data)

    if errors:
        return jsonify(errors), 400

    plan = LessonPlan(
        title=data['title'],
        objective=data['objective'],
        summary=data['summary'],
        discipline=data['discipline'],
        contents=data.get('contents'),
        resources=data.get('resources'),
        tags=data.get('tags')
    )

    db.session.add(plan)

    db.session.commit()

    return jsonify({
        "message": "Plano criado com sucesso"
    }), 201


# READ ALL
@app.route('/plans', methods=['GET'])
def get_plans():

    plans = LessonPlan.query.all()

    result = []

    for plan in plans:

        result.append({
            "id": plan.id,
            "title": plan.title,
            "objective": plan.objective,
            "summary": plan.summary,
            "discipline": plan.discipline,
            "contents": plan.contents,
            "resources": plan.resources,
            "tags": plan.tags
        })

    return jsonify(result)


# READ BY ID
@app.route('/plans/<int:id>', methods=['GET'])
def get_plan(id):

    plan = LessonPlan.query.get_or_404(id)

    return jsonify({
        "id": plan.id,
        "title": plan.title,
        "objective": plan.objective,
        "summary": plan.summary,
        "discipline": plan.discipline,
        "contents": plan.contents,
        "resources": plan.resources,
        "tags": plan.tags
    })


# UPDATE
@app.route('/plans/<int:id>', methods=['PUT'])
def update_plan(id):

    plan = LessonPlan.query.get_or_404(id)

    data = request.json

    errors = schema.validate(data)

    if errors:
        return jsonify(errors), 400

    plan.title = data['title']
    plan.objective = data['objective']
    plan.summary = data['summary']
    plan.discipline = data['discipline']
    plan.contents = data.get('contents')
    plan.resources = data.get('resources')
    plan.tags = data.get('tags')

    db.session.commit()

    return jsonify({
        "message": "Plano atualizado com sucesso"
    })


# DELETE
@app.route('/plans/<int:id>', methods=['DELETE'])
def delete_plan(id):

    plan = LessonPlan.query.get_or_404(id)

    db.session.delete(plan)

    db.session.commit()

    return jsonify({
        "message": "Plano removido com sucesso"
    })


# HEALTH CHECK
@app.route('/health', methods=['GET'])
def health():

    return jsonify({
        "status": "ok"
    })