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

    static streamResponse(thread_id, onMessageCallback, onErrorCallback, onCompleteCallback){
        const eventSource = new EventSource(`${BASE_URL}/graph/stream/${thread_id}`)

        eventSource.addEventListener('token', (event)=>{
            try {
                const data = JSON.parse(event.data)
                onMessageCallback({
                    content: data.content
                })
            } catch (error) {
                console.error("Error parsing token event:", error, "Raw data:", event.data)
            }
        })
    }
}


export default assistantService