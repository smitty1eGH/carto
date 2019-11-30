from flask import Flask,escape,request,render_template
from flask_cors import CORS
from geojson_rewind import rewind
from postgres import Postgres
CONN="postgresql://postgres@127.0.0.1:5432/cartodb_dev_user_1990ea72-de88-4086-8074-88136aadbf34_db"
db=Postgres(url=CONN)

app = Flask(__name__)
CORS(app, supports_credentials=True)

SQL="""
SELECT jsonb_build_object(      'type','GeometryCollection','features', jsonb_agg(feature)  )
FROM (SELECT jsonb_build_object('type','MultiPolygon','id', gid,'geometry',ST_AsGeoJSON(the_geom)::jsonb,'properties'
                               , to_jsonb(inputs) - 'type' - 'gid' - 'the_geom') AS feature
      FROM (SELECT *
            FROM (SELECT the_geom, geoid10 AS gid, COALESCE(turnout,0) AS turnout
                  FROM  (SELECT ST_ForceRHR(the_geom) as the_geom
                              , geoid10, CASE WHEN COALESCE (pop_density,0) > 0 THEN CAST(tot_votes/pop_density AS INTEGER) END AS turnout
                         FROM   tl_2012_vtd10_pop
                         WHERE  statefp10 = '51') AS va
                         LIMIT  1      
                        ) raw
                 ) inputs
           ) features;"""


@app.route('/')
def asdf(name=None):
    res={}
    with db.get_cursor() as cursor:
        res["cartodata"]=str(rewind(cursor.all(SQL)[0])).replace("'",'"')

    return render_template('app.html',res=res)


@app.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

if __name__=='__main__':
    app.run()
