import React, { useState, useEffect } from 'react';
import InputBox from './InputBox';
import Message from './Message';
import { ApiCall } from './Api';


export default function ChatWindow() {
    const [questionsAndAnswers, setQuestionsAndAnswers] = useState([]);

    const handleQuestionSubmit = async (question) => {
        setQuestionsAndAnswers(prevState => [...prevState, { question, answer: '' }]); // Render the question immediately

        try {
            const responseData = await ApiCall(question);
            updateAnswer(responseData.message, question); // Update the answer once the response is received
        } catch (error) {
            console.error('Error fetching data:', error);
            updateAnswer('An error occurred while fetching data.', question); // Handle error
        }
    };

    const updateAnswer = (answer, question) => {
        setQuestionsAndAnswers(prevState =>
            prevState.map(qa => (qa.question === question ? { ...qa, answer } : qa))
        );
    };

    return (
        <div style={{ overflowY: 'auto', maxHeight: '80vh', padding: '10px',}}> {/* Add styling to prevent overlapping */}
            {questionsAndAnswers.map((qa, index) => (
                <div key={index}>
                    <Message question={qa.question} />
                    {qa.answer && <Message question={qa.answer} />} {/* Render the answer if available */}
                </div>
            ))}
            <InputBox onSubmit={handleQuestionSubmit} />
        </div>
    );
}




// export default function ChatWindow(){
//     const [question, setQuestion] = useState('');
//     const [response, setResponse] = useState(null);
//     // useEffect hook to fetch data from the API when the component mounts or question changes
//     useEffect(() => {
//         const fetchData = async () => {
//             if (question.trim() !== '') { // Only fetch data if the question is not empty
//                 try {
//                     const responseData = await ApiCall(question);
//                     setResponse(responseData); // Update component state with the response from the API
//                 } catch (error) {
//                     console.error('Error fetching data:', error);
//                 }
//             }
//         };
//         fetchData(); // Call the fetchData function
//     }, [question]); // Run useEffect whenever the question state changes

//     const handleQuestionSubmit = (question) => {
//         setQuestion(question)
//         setResponse(null);
//     }
//     return(
//         <>
//         <div>
//             <Message question={question} />
//             {console.log('Response condition:', response)} {/* Log the condition */}
//             {response && <Message question={response.message} />} {/* Render the response message if available */}
//             <InputBox onSubmit={handleQuestionSubmit} />
//         </div>
//         </>
//     )
// }