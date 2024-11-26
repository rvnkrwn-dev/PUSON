import {GoogleGenerativeAI} from "@google/generative-ai"

export default defineEventHandler(async (event) => {
    try {
        const genAI = new GoogleGenerativeAI("AIzaSyAfEl7SIVhQ0x03NupoPAbw03jmzr60Bq4");
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash"});
        const prompt = "Tuliskan lagu indonesia raya."

        const result = await model.generateContent(prompt);
        const response = await result.response;
        const text = response.text();
        console.log(text);
    } catch (err) {

    }
})