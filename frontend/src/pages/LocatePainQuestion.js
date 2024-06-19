import React, { useState } from 'react';
import "../styles/LocatePainQuestion.css";
import { useNavigate } from 'react-router-dom';
import Body from "../assets/photos/LocatePain.png";

function LocatePainQuestion() {
    const [selectedAreas, setSelectedAreas] = useState([]);

    const navigate = useNavigate();

    const handleButtonClick = (area) => {
        setSelectedAreas(prevSelected => 
            prevSelected.includes(area) 
                ? prevSelected.filter(item => item !== area) 
                : [...prevSelected, area]
        );
    };

    const handleContinueClick = () => {
        const formData = selectedAreas.reduce((acc, area) => {
            acc[area] = true;
            return acc;
        }, {});
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
                            className={`body-button ${selectedAreas.includes(area) ? 'selected' : ''}`}
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
