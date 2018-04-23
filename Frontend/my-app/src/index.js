import React from 'react'
import { render } from 'react-dom'
//import { hello, goodbye } from './lib'
import { SkiDayCount } from './components/SkiDayCount'

render(
    <SkiDayCount    total={50}
                    powder={20}
                    backcountry={10}
                    goal={100}/>,
    document.getElementById('react-container')
)