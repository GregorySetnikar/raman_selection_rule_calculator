const express = require('express');
const path = require('path');
const katex = require('katex');
let {PythonShell} = require('python-shell')
const app = express();
const port = process.env.PORT || 8080;

app.use(express.static('public'))

app.get('/', function(req, res) {
    res.sendFile(path.resolve(__dirname, 'public', 'index.html'));
});

app.get('/api', function (req, res) {
    const params = req.query;

    let options = {
        mode: 'text',
        //pythonPath: 'path/to/python',
        args: [params.space_group,params.pointing_vector,params.ref_axis,params.polar_in,params.polar_out,params.angle,params.pointing_vector_x,params.pointing_vector_y,params.pointing_vector_z,params.ref_axis_x,params.ref_axis_y,params.ref_axis_z,params.database]
    };
      
    const pathScript = path.resolve(__dirname, 'public/python', 'computer.py');

    PythonShell.run(pathScript, options, function (err, results) {
        if (err) {
            console.error(err);
            res.status(400).send('<h1>ERROR 400</h1>');
        } else {
            res.json(results);
        }
    });
    
})

app.listen(port, () => {
    console.log('Server app at http://localhost:' + port);
});

