import json

SLASH_O='/tmp/va.json' #psql \o target
PROTO='/home/ubuntu/proj/carto/carto/rough.html'

def first_and_last(s,c=30):
    print(s[0:c])
    print(s[-c:])

def write_sample(x,y):
    the_data='{x:%s,y:%s}' % (x[0:10],y[0:10])
    templ='''
    <html><head>
    <meta charset="utf-8">
    <script src="static/d3-array.v2.min.js"></script>
    <script src="static/d3-axis.v1.min.js"></script>
    <script src="static/d3-color.v1.min.js"></script>
    <script src="static/d3-dsv.v1.min.js"></script>
    <script src="static/d3-fetch.v1.min.js"></script>
    <script src="static/d3-format.v1.min.js"></script>
    <script src="static/d3-interpolate.v1.min.js"></script>
    <script src="static/d3-path.v1.min.js"></script>
    <script src="static/d3-time.v1.min.js"></script>
    <script src="static/d3-time-format.v2.min.js"></script>
    <script src="static/d3-scale.v3.min.js"></script>
    <script src="static/d3-scale-chromatic.v1.min.js"></script>
    <script src="static/d3-selection.v1.min.js"></script>
    <script src="static/d3-shape.v1.min.js"></script>

    <script src="static/workly.min.js"></script>
    <script src="static/rough.min.js"></script>

    <script src="static/d3-shape.v1.min.js"></script>
    <style>
	    .wrapper {
	      display: flex;
	      flex:    wrap;
              order:   row;
	    }
    </style>
    </head><body>
      <div class="wrapper">
        <div id="viz0"></div>
      </div>
    <script>
new roughViz.Scatter(  { element  : '#vis0'
    , data: %s         , title    : 'Turnout as a function of population density'
    , x   : 'x'        , y        : 'y'
    , colorVar: ''     , highlightLabel: ''
    , fillWeight: 4    , radius   : 12
    , colors: ['black'], stroke   : 'black'
    , strokeWidth: 0.4 , roughness: 1
    , width: 400       , height   : 450
    , font: 0          , xLabel   : 'population per square meter'
    , yLabel: 'turnout', curbZero : false,
})
    <script>
    </body><html>
    ''' % the_data
    with open(PROTO,'w') as f:
        f.write(templ)

with open(SLASH_O) as f:
    '''The idea is to make one trip to the database with the criteria, and 
       be able to pull out a list of JSON stringage and then transform it
       into browser-read data.
       Also to be able to export from the DB to a file and split the system
       apart. Alas, there is messiness to this approach.
    '''
    f.readline()  #field label
    f.readline()  #-----------
    g=f.readline()[:-5] + '}]'
    h=json.loads(g)
    i=json.loads('{' + h[0]['concat'])
    x=[]
    y=[]
    for j in i['data']:
        x.append(j['pd'])
        y.append(j['vs'])
    write_sample(x,y)

   #print(f.readline()[:-6]+']' )
   # h=json.loads(f.readline()[:-1])

