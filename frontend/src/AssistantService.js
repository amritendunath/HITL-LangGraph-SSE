import axios from 'axios'

const BASE_URL = process.env.BASE_URL

class assistantService {
    //API Methods: REST
    static async startConversation(human_req) {
        try {
            const response = await axios({
                url: `${BASE_URL}/graph/start`,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(human_req)
            })
            if (response.status >= 200 && response.status < 300) {
                return response.json() | response.data
            }
            else {
                console.error("Server responded with error", response.status, response.data)
            }
        } catch (error) {
            console.log("Error starting conversations", error)
        }
    }

    // static async submitReview({

    // })
    //API Methods: SSE
    static async createStreamingConversation(human_req){
        try {
            const response = await axios({
                url: `${BASE_URL}/graph/stream/create`,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(human_req)
            })
            if (response.status >= 200 && response.status < 300){
                return response.json() | response.data
            }
            else{
                console.error("Server responded with error", response.status, response.data)
            }
        } catch (error) {
            console.log("Error from server side", error)
        }
    }
}

export default assistantService