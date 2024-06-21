import React, { useState } from 'react';
import "../styles/LocatePainQuestion.css";
import { useNavigate } from 'react-router-dom';
import Body from "../assets/photos/LocatePain.png";
import Logo from "../assets/photos/brig.png"

function LocatePainQuestion() {
    const initialFormData = {
        "Abdominal pain / pressure": 0,
        "Pelvic pain": 0,
        "Lower back pain": 0,
        "Vaginal Pain/Pressure": 0,
        "Bowel pain": 0,
    };

    const [formData, setFormData] = useState(initialFormData);
    const navigate = useNavigate();

    // Mapping between UI display and formData keys
    const bodyAreas = [
        { key: "Abdominal pain / pressure", label: "Abdomen" },
        { key: "Pelvic pain", label: "Pelvic area" },
        { key: "Lower back pain", label: "Lower back" },
        { key: "Vaginal Pain/Pressure", label: "Vaginal area" },
        { key: "Bowel pain", label: "Bowel area" },
    ];

    const handleButtonClick = (areaKey) => {
        // Update formData
        setFormData(prevFormData => ({
            ...prevFormData,
            [areaKey]: prevFormData[areaKey] === 1 ? 0 : 1 // Toggle between 0 and 1
        }));
    };

    const handleContinueClick = () => {
        console.log(formData);

        // Send formData to the backend
        fetch('http://127.0.0.1:5000/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            navigate('/fillq', { state: { data } });
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    };

    const handleBackClick = () => {
        navigate("/");
    };

    return (
        <div className='question-screen'>
            <div className='frame'>
                <button className='back' onClick={handleBackClick}>Back</button>
                <img src={Logo} className='corner-logo'/>
                <div className='locate-pain'> Please specify the location of pain. </div>
                <div className='image'>
                    <img src={Body} className='body'/>
                </div>
                <div className='area-buttons'>
                    {bodyAreas.map((area, index) => (
                        <button
                            key={index}
                            className={`body-button ${formData[area.key] === 1 ? 'selected' : ''}`}
                            onClick={() => handleButtonClick(area.key)}
                        >
                            {index + 1}. {area.label}
                        </button>
                    ))}
                </div>
                <div className='button-frame'>
                    <button className='continue-button' onClick={handleContinueClick}>
                        Continue
                    </button>
                </div>
            </div>
        </div>
    );
}

export default LocatePainQuestion;
