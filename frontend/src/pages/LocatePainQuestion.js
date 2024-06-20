import React, { useState } from 'react';
import "../styles/LocatePainQuestion.css";
import { useNavigate } from 'react-router-dom';
import Body from "../assets/photos/LocatePain.png";

function LocatePainQuestion() {
    const initialFormData = {
        "Abdomen": 0,
        "Pelvic area": 0,
        "Lower back": 0,
        "Vaginal area": 0,
        "Bowel area": 0,
    };

    const [formData, setFormData] = useState(initialFormData);

    const navigate = useNavigate();

    const handleButtonClick = (area) => {
        setFormData(prevFormData => ({
            ...prevFormData,
            [area]: 1
        }));
    };

    const handleContinueClick = () => {
        console.log(formData);

        fetch('http://127.0.0.1:5000/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            navigate('/results', { state: { data } });
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    };

    const handleBackClick = () => {
        navigate("/");
    }

    return (
        <div className='question-screen'>
            <div className='frame'>
                <button className='back' onClick={handleBackClick}>Back</button>
                <div className='locate-pain'> Please specify the location of pain. </div>
                <div className='image'>
                    <img src={Body} className='body'/>
                </div>
                <div className='area-buttons'>
                    {['Abdomen', 'Pelvic area', 'Lower back', 'Vaginal area', 'Bowel area'].map((area, index) => (
                        <button
                            key={index}
                            className={`body-button ${formData[area] === 1 ? 'selected' : ''}`}
                            onClick={() => handleButtonClick(area)}
                        >
                            {index + 1}. {area}
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
