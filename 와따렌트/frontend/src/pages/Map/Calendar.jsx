// import React, { useState } from 'react' 
// import Calendar1 from 'react-calendar'
// import 'react-calendar/dist/Calendar.css'

// export default function Calendar() {
//     const [ value, onChange ] = useState(new Date())

//     return (
//         <div>
//             <Calendar1 onChange={onChange} value={value} />
//         </div>
//     )
// }
import React, {useState} from "react";
import Datepicker from "react-tailwindcss-datepicker";

const Calendar = () => {
    const [value, setValue] = useState({
        startDate: "",
        endDate: ""
    });
    
    const handleValueChange = (newValue) => {
        console.log("newValue:", newValue);
        setValue(newValue);
    }
    
    return (
        <div>
          <h2 >시작 날짜와 종료 날짜를 선택해주세요</h2>
          <hr/>
            <Datepicker
                value={value}
                onChange={handleValueChange}
                separator={"~"} 
                // showFooter={true} 
                useRange={false} 
                minDate={new Date()} 
                maxDate={new Date("2023-12-31")} 
            />
        </div>
    );
};

export default Calendar;