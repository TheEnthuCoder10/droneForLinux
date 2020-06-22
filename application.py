from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

defaultDATA = {
    'D001': {"FCVolt(V1)": 48.5,
             "FCVolt(V2)": 45.7,
             "FCPres": 1.5,
             "FCCurr": 150.4,
             "DroneRunning": True},

}


def abort_if_drone_doesnt_exist(drone_id):
    if drone_id not in defaultDATA:
        abort(404, message="Drone {} doesn't exist".format(drone_id))


parser = reqparse.RequestParser()
parser.add_argument('FCVolt(V1)')
parser.add_argument('FCVolt(V2)')
parser.add_argument('FCPres')
parser.add_argument('FCCurr')


class F2(Resource):
    def get(self, drone_id):
        abort_if_drone_doesnt_exist(drone_id)
        return defaultDATA[drone_id]


class F1(Resource):
    def get(self):
        if True:
            return defaultDATA
        else:
            return jsonify({"DroneRunning": False})

    def post(self):
        args = parser.parse_args()
        drone_id = 'D00%d' % (len(defaultDATA) + 1)
        defaultDATA[drone_id] = {'FCVolt(V1)': args['FCVolt(V1)'],
                                 "FCVolt(V2)": args["FCVolt(V2)"],
                                 "FCPres": args["FCPres"],
                                 "FCCurr": args["FCCurr"],
                                 "DroneRunning": True}
        return jsonify({"Success": True})


api.add_resource(F1, '/api/v1/droneList')
api.add_resource(F2, '/api/v1/droneList/<string:drone_id>')

if __name__ == '__main__':
    app.run(debug=True)
