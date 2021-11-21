// $(document).ready(function(){
//     console.log("Script loaded \n document ready");
// //     $("#cancer-type").change(function() {

// //         var networkSelected = 'GDIN'

// //         // $("#network").change(function(){
// //         //     networkSelected = $(this).find(':selected').val()
// //         // })

// //         var selectedVal = $(this).find(':selected').val()

// //         if(networkSelected == 'GDIN'){
// //             $.getJSON(`../../networks/Gene-drug interaction network/${selectedVal}.json`, function (data) {
// //                 console.log(data);
// //                 var cy = cytoscape({
// //                     container: document.querySelector(".network-container"),
// //                     elements: data,
// //                     style: [
// //                         {
// //                             selector: 'node',
// //                             style: {
// //                                 'label': 'data(label)',
// //                                 'width': '60px',
// //                                 'height': '60px',
// //                                 'color': 'blue',
// //                                 'background-fit': 'contain',
// //                                 'background-clip': 'none'
// //                             }
// //                         }, {
// //                             selector: 'edge',
// //                             style: {
// //                                 'text-background-color': 'yellow',
// //                                 'text-background-opacity': 0.4,
// //                                 'width': '6px',
// //                                 'target-arrow-shape': 'triangle',
// //                                 'control-point-step-size': '140px'
// //                             }
// //                         }
// //                     ],
// //                     layout: {
// //                         name: 'circle'
// //                     }
// //                 });
// //             });
// //         }


// //     });
// // })

$(document).ready(function(){
    console.log("Script loaded \n document ready");
    $("#cancer-type").change(function(){
        console.log("cy loaded");
        var cy = cytoscape({
            container: document.getElementById('cy'),
            elements: [{
                group: 'nodes',

                data: {
              "id": "n1",
              "parent": "nparent",
            },

                scratch: {
              "_foo": "bar"
            },

                position: {
                  x: 100,
                  y: 100
            },

                selected: false,

                selectable: true,

                locked: false,

                grabbable: true,

                pannable: false,

                classes: ['foo', 'bar'],
            style: [
                {
                    selector: 'node',
                    style: {
                        'label': 'data(label)',
                        'width': '60px',
                        'height': '60px',
                        'color': 'blue',
                        'background-fit': 'contain',
                        'background-clip': 'none'
                    }
                }, {
                    selector: 'edge',
                    style: {
                       'text-background-color': 'yellow',
                        'text-background-opacity': 0.4,
                        'width': '6px',
                        'target-arrow-shape': 'triangle',
                        'control-point-step-size': '140px'
                    }
                }
            ],
            layout: {
                name: 'circle'
            }
        }]
    })



})
})