from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
import logging

from get_tissue_with_w2v import Tissue

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('disease')
parser.add_argument('n')

tissue = Tissue(loggerLevel=logging.DEBUG)
tissue.calculate_background(1_000) # TODO: Need to increase this number via multiprocessing

print("Setup complete!")

class GetTissue(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        args = parser.parse_args()
        
        try: 
            out = tissue.get_distance(args['disease'], n=int(args['n']), compare_with_background=True)

        except KeyError: 
            return "Disease not found in corpus!", 400

        except IndexError: 
            return "n greater than the number of tissues!", 400
        
        out = {
            'result': [
                {
                    'tissue':i, 
                    'score': '{:6.4f}'.format(j), 
                    'percentile': '{:7.4f}'.format(k)
                } for i,j,k in out
            ]
        }
        out = json.dumps(out)

        return out, 200

api.add_resource(GetTissue, '/')

if __name__ == '__main__':
    app.run(debug=False)
