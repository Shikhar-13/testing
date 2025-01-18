
from flask import render_template ,url_for, request ,jsonify ,redirect
from app import app
from .main import VoiceAgent, VoiceAgentConfig, AgentPresets
from dotenv import load_dotenv
from supabase import create_client, Client
import asyncio
import os
from .Id import TaskIDGenerator



SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return render_template('voice-agent.html', title='Home Page')

@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    if request.method != 'POST':
        return redirect(url_for('home'))
    file = request.form.get('file')
    date = request.form.get('date')
    time = request.form.get('time')
    timezone = request.form.get('timezone')
    voice_id = (request.form.get('voice_id'))

    # Validate required fields
    required_fields = {
        'file': file,
        'date': date,
        'time': time,
        'timezone': timezone,
        'voice_id': voice_id
    }
    
    # missing_fields = [field for field, value in required_fields.items() if not value]
    # if missing_fields:
    #     return jsonify({
    #         'status': 'error',
    #         'message': f'Missing required fields: {", ".join(missing_fields)}'
    #     }), 400

    try:
        # Insert the task into the Supabase table
        data = {
            'file': file,
            'date': date,
            'Time': time,
            'Timezone': timezone,
            'Voice_id': voice_id,
        }
        
        response = supabase.table('tasks').insert(data).execute()
        
        # Check if data was inserted successfully
        if response.data:
            
            return redirect(url_for('home'))
        
        
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to create task'
            }), 400
            
    except Exception as e:
        app.logger.error(f"Error creating task: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error occurred'
        }), 500



@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    pass


@app.route('/add_agent', methods=["GET",'POST'])
def add_agent():
    api_key = os.getenv("RETELL_API_KEY")
    if not api_key:
        return jsonify({"error": "RETELL_API_KEY not found in environment variables"}), 500
    
    call_type = request.form.get('call_type')
    task_id = request.form.get('task_id')
    response = supabase.table("tasks").select("Voice_id").eq("Task_id", task_id).execute()
    voice_id = response.data[0]["Voice_id"] if response.data else None
    # Validate task_id since it's a foreign key
    if not task_id:
        return jsonify({"error": "task_id is required"}), 400

    async def process():
        agent = VoiceAgent(api_key, config=VoiceAgentConfig(
            llm_id="llm_f1fbe2eefad955e589c03fa8040c",
            llm_type="retell-llm",  # Use the correct LLM type
            voice_id=voice_id,  # Set the appropriate voice ID
        ))
        
        agent_id = await agent.create_agent()
        return {"agent_id": agent_id}
    
    
    try:
        # Create new event loop for async operation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run the async process
        response = loop.run_until_complete(process())
        loop.close()

        # Check for errors in agent creation
        if "error" in response:
            return jsonify(response), 500

        # Prepare data for Supabase
        data = {
            'agent_id': response['agent_id'],
            'call_type': call_type,
            'task_id': task_id  # Include task_id in the data
        }

        # Insert into Supabase
        db_response = supabase.table('agents').insert(data).execute()
        
        # Verify successful insertion
        if not db_response.data:
            return jsonify({"error": "Failed to insert agent data into database"}), 500

        return redirect(url_for('home'))

    except Exception as e:
        # Log any unexpected errors
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        # Ensure the loop is closed even if an error occurs
        if 'loop' in locals() and loop.is_running():
            loop.close()



@app.route('/get_agent', methods=['GET'])
def get_agent():
    pass    