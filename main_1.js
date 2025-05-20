import React, { useState } from "react";
import axios from "axios";

function App() {
    const [purpose, setPurpose] = useState("");
    const [budget, setBudget] = useState(0);
    const [recommendation, setRecommendation] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await axios.post("http://localhost:8000/recommend", {
            purpose,
            budget,
        });
        setRecommendation(response.data);
    };

    return (
        <div>
            <h1>AI 부품 추천</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    용도:
                    <select value={purpose} onChange={(e) => setPurpose(e.target.value)}>
                        <option value="gaming">게임</option>
                        <option value="editing">편집</option>
                        <option value="general">일반</option>
                    </select>
                </label>
                <br />
                <label>
                    예산:
                    <input
                        type="number"
                        value={budget}
                        onChange={(e) => setBudget(e.target.value)}
                    />
                </label>
                <br />
                <button type="submit">추천 받기</button>
            </form>

            {recommendation && (
                <div>
                    <h2>추천 부품</h2>
                    <p>CPU: {recommendation.CPU}</p>
                    <p>GPU: {recommendation.GPU}</p>
                    <p>가격: {recommendation.Price}</p>
                </div>
            )}
        </div>
    );
}

export default App;
