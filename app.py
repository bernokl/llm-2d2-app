from flask import Flask, render_template, request
import openai
import os
import subprocess
import re
import time

app = Flask(__name__)

# Set your OpenAI API key from environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    d2_code = ''
    image_path = ''
    timestamp = ''
    if request.method == 'POST':
        description = request.form['description']
        d2_code = get_d2_code(description)

        # Save the D2 code to a file
        with open('diagram.d2', 'w') as f:
            f.write(d2_code)

        # Render the D2 code to SVG using D2 CLI
        subprocess.run(['d2', 'diagram.d2', 'static/diagram.svg'])
        image_path = 'static/diagram.svg'

        # Generate a timestamp to force image reload
        timestamp = int(time.time())

    return render_template('index.html', d2_code=d2_code, image_path=image_path, timestamp=timestamp)



def get_d2_code(description):
    messages = [
        {
            "role": "system",
            "content": """You are an expert AWS cloud architect specializing in creating domain-focused diagrams of AWS cloud infrastructure using D2 code. Your diagrams should accurately represent AWS services and components, using appropriate labels and relationships to depict the infrastructure flow. Please avoid any markdown formatting and provide only the D2 code.

Example:

elbs: {
  label: "ELBs"
  elb1: "ELB 1"
  elb2: "ELB 2"
}

aws_vpc: {
  label: "AWS VPC"

  zone1: {
    label: "| Zone 1 |"
    width: 430
  }

  zone2: {
    label: "| Zone 2 |"
    width: 430
  }

  zone3: {
    label: "| Zone 3 |"
    width: 430
  }

  eks_cluster: {
    label: "EKS Cluster"
    deployments: {
      muesly_swap_proxy: "Muesly Swap Proxy"
      congeco_proxy: "Congeco Proxy"
      posthog_proxy: "Posthog Proxy"
      cardano_core: {
        label: "Cardano Stack"
        cardano_node: "Cardano Node"
        cardano_db_sync: "Cardano db-sync"
        ogmios: "Ogmios"
        postgres: "Postgres"
        metadata_sync: "Metadata Sync"
      }
      helm_deployment_core: {
            label: "posthog-posthog-proxy"
            shape: square
            style.fill: "#6699ff"
        }
      cardano_services: {
        label: "Cardano Services"
        projectors: "Projectors"
        providers: "Providers"
      }
    }
  }
}

elbs.elb1 -> aws_vpc
elbs.elb2 -> aws_vpc

aws_vpc.zone1 -> aws_vpc.eks_cluster
aws_vpc.zone2 -> aws_vpc.eks_cluster
aws_vpc.zone3 -> aws_vpc.eks_cluster

"""
        },
        {
            "role": "user",
            "content": f"""Transform the following description into D2 code that represents an AWS cloud infrastructure diagram.

Please ensure that:
- All AWS services are represented accurately.
- Components are labeled with their AWS service names (e.g., EC2, S3, Lambda).
- Relationships and data flows between components are clearly depicted.
- Use grouping or clusters for related services when appropriate.
- Avoid any markdown formatting; provide only the D2 code.

Description:

{description}

D2 code:"""
        }
    ]

    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            max_tokens=500,
            temperature=0,
        )
        d2_code = response['choices'][0]['message']['content'].strip()

        # Remove code block formatting (triple backticks and any enclosed text)
        d2_code = re.sub(r"```[\s\S]*?```", '', d2_code)
        # Remove any remaining backticks
        d2_code = d2_code.replace('`', '')
        # Remove any instance of "plaintext" labels
        d2_code = d2_code.replace('plaintext', '')

        return d2_code.strip()
    except openai.error.OpenAIError as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

