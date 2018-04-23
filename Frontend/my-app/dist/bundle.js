'use strict';

//const { createElement } = React
var _ReactDOM = ReactDOM,
    render = _ReactDOM.render;


var style = {
    backgroundColor: 'orange',
    color: 'white',
    fontFamily: 'verdana'

    /*const title = createElement(
        'h1',
        {id: 'title', className: 'header', style: style},
        'Group Scheduler'
    )*/

};render(React.createElement(
    'h1',
    { id: 'title',
        className: 'header',
        style: style },
    'Group Scheduler'
), document.getElementById('react-container'));
