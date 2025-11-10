from kubernetes import client, config
import json
import sys

# Dettagli del Deployment 
NAMESPACE = "formazione-sou"
DEPLOYMENT_NAME = "flask-app-release-flask-app-chart" 

def export_deployment_details():
    try:
        # Tenta di caricare la configurazione in-cluster (Service Account)
        config.load_incluster_config()
    except config.config_exception.ConfigException:
        # Se fallisce, carica il kubeconfig locale
        config.load_kube_config()
    
    apps_v1 = client.AppsV1Api()
    
    try:
        deployment = apps_v1.read_namespaced_deployment(name=DEPLOYMENT_NAME, namespace=NAMESPACE)
        container = deployment.spec.template.spec.containers[0]
        
        # Controllo che ci siano tutte le specifiche
        validation_errors = []

        # 1. Verifica Liveness Probe
        if not container.liveness_probe:
            validation_errors.append("Manca il Liveness Probe.")

        # 2. Verifica Readiness Probe
        if not container.readiness_probe:
            validation_errors.append("Manca il Readiness Probe.")

        # 3. Verifica Limits & Requests (Risorse)
        # Controlla che il blocco resources esista e che limits/requests non siano None
        if not container.resources or not container.resources.limits or not container.resources.requests:
            validation_errors.append("Mancano Limits e/o Requests (risorse).")
        
        # Gestisce errore in caso manchi qualcosa
        if validation_errors:
            error_message = "\n".join(validation_errors)
            # Solleva un'eccezione standard con il messaggio dettagliato di cosa manca
            raise Exception(f"Il Deployment ha fallito le verifiche essenziali:\n{error_message}")
        
        # Se la validazione ha successo, esegue l'export
        
        # ... (Codice per l'export dei dati JSON) ...

        print("\nVALIDAZIONE SUPERATA. Dettagli Deployment Esportati:")
        print(json.dumps({
            "metadata": {"name": deployment.metadata.name},
            "status": {"replicas_ready": deployment.status.ready_replicas}
        }, indent=2))
        
    except client.ApiException as e:
        # Cattura errori di comunicazione o permessi (es. 403 Forbidden)
        print(f"Errore API durante l'accesso al Deployment: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Cattura l'eccezione standard (inclusi gli errori di validazione sollevati sopra)
        print(f"\nFATAL: Errore di Validazione/Esecuzione:\n{e}", file=sys.stderr)
        sys.exit(1) # Forza l'uscita con codice di errore, facendo fallire Jenkins

if __name__ == "__main__":
    export_deployment_details()