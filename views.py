from flask import request, Blueprint
from flask_cors import cross_origin

from controllers.signup import FrequentlyAskedQuestionController

blueprint = Blueprint('main', __name__)


@blueprint.route("/faq", methods=['POST'])
@cross_origin()
def frequently_asked_question():
    return FrequentlyAskedQuestionController(request).call()
