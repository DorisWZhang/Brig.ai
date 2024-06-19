import React, { useState } from 'react';
import "../styles/FillQuestion.css";
import { useNavigate } from 'react-router-dom';

function FillQuestion() {
    const [formData, setFormData] = useState({
        age: '',
        height: '',
        systolicBP: '',
        diastolicBP: '',
        bloodType: '',
        pulse: '',
        rr: '',
        periodCycleLength: '',
        numberOfAbortions: ''
    });
    const navigate = useNavigate();

    const handleInputChange = (e) => {
        const { id, value } = e.target;
        setFormData({ ...formData, [id]: value });
    };

    const handleContinueClick = () => {
        // Handle continue button click
        console.log(formData);
        // You can add your logic here, e.g., navigating to another page
    };

    const handleBackClick = () => {
        // Handle back button click
        navigate(-1); // This will navigate back to the previous page
    };

    return (
        <div className='question-screen'>
            <div className='frame'>
                <button className='back' onClick={handleBackClick}>Back</button>
                <div className='input-groups'>
                    <div className='row-1'> 
                    <div className='input-group'>
                        <label htmlFor='age'>Age:</label>
                        <input
                            type='number'
                            id='age'
                            value={formData.age}
                            onChange={handleInputChange}
                            placeholder='Enter your age'
                        />
                    </div>
                    <div className='input-group'>
                        <label htmlFor='height'>Height (cm):</label>
                        <input
                            type='number'
                            id='height'
                            value={formData.height}
                            onChange={handleInputChange}
                            placeholder='Enter your height in cm'
                        />
                    </div>
                    <div className='input-group'>
                        <label htmlFor='systolicBP'>Systolic Blood Pressure (mmHg):</label>
                        <input
                            type='number'
                            id='systolicBP'
                            value={formData.systolicBP}
                            onChange={handleInputChange}
                            placeholder='Enter your systolic BP in mmHg'
                        />
                    </div>
                    <div className='input-group'>
                        <label htmlFor='diastolicBP'>Diastolic Blood Pressure (mmHg):</label>
                        <input
                            type='number'
                            id='diastolicBP'
                            value={formData.diastolicBP}
                            onChange={handleInputChange}
                            placeholder='Enter your diastolic BP in mmHg'
                        />
                    </div>
                    </div>
                    <div className='row-2'>
                    <div className='input-group'>
                        <label htmlFor='bloodType'>Blood Type:</label>
                        <input
                            type='text'
                            id='bloodType'
                            value={formData.bloodType}
                            onChange={handleInputChange}
                            placeholder='Enter your blood type'
                        />
                    </div>
                    
                    
                    <div className='input-group'>
                        <label htmlFor='pulse'>Pulse (bpm):</label>
                        <input
                            type='number'
                            id='pulse'
                            value={formData.pulse}
                            onChange={handleInputChange}
                            placeholder='Enter your pulse in bpm'
                        />
                    </div>
                    <div className='input-group'>
                        <label htmlFor='rr'>Respiratory Rate (breaths/min):</label>
                        <input
                            type='number'
                            id='rr'
                            value={formData.rr}
                            onChange={handleInputChange}
                            placeholder='Enter your respiratory rate in breaths/min'
                        />
                    </div>
                    
                    
                        <div className='input-group'>
                            <label htmlFor='periodCycleLength'>Period Cycle Length (days):</label>
                            <input
                                type='number'
                                id='periodCycleLength'
                                value={formData.periodCycleLength}
                                onChange={handleInputChange}
                                placeholder='Enter your period cycle length in days'
                            />
                        </div>
                        </div>
                        <div className='row-3'>
                        <div className='input-group'>
                            <label htmlFor='numberOfAbortions'>Number of Abortions:</label>
                            <input
                                type='number'
                                id='numberOfAbortions'
                                value={formData.numberOfAbortions}
                                onChange={handleInputChange}
                                placeholder='Enter the number of abortions'
                            />
                        </div>
                    </div>
                </div>
                <div className='button-frame'>
                    <button className='continue-button' onClick={handleContinueClick}>
                        {'Continue'}
                    </button>
                </div>
            </div>
        </div>
    );
}

export default FillQuestion;
