from kubernetes import client, config
import json

# --- Configurazione Service Account ---
# Se lo script è eseguito all'interno di un Pod che utilizza il Service Account 'cluster-reader',
# questa funzione carica automaticamente la configurazione interna.
# Altrimenti, useresti 'config.load_kube_config()' per un accesso esterno.
try:
    config.load_incluster_config()
    print("Configurazione caricata utilizzando il Service Account in-cluster.")
except config.config_exception.ConfigException:
    print("Esecuzione esterna al cluster. Caricamento kubeconfig...")
    config.load_kube_config() # Funziona se il file kubeconfig è disponibile.


# --- Dettagli del Deployment ---
NAMESPACE = "formazione-sou"  # Sostituisci con il namespace corretto
DEPLOYMENT_NAME = "flask-app-release-flask-app-chart" # Sostituisci con il nome del tuo Deployment

def export_deployment_details():
    # client.AppsV1Api() è l'API per lavorare con Deployment, DaemonSet, ecc.
    apps_v1 = client.AppsV1Api()

    try:
        # Recupera l'oggetto Deployment
        deployment = apps_v1.read_namespaced_deployment(name=DEPLOYMENT_NAME, namespace=NAMESPACE)
        
        # --- Export dei Dettagli Chiave ---
        
        # 1. Metadati
        metadata = {
            "name": deployment.metadata.name,
            "namespace": deployment.metadata.namespace,
            "uid": deployment.metadata.uid,
            "creation_timestamp": str(deployment.metadata.creation_timestamp)
        }
        
        # 2. Stato (Status)
        status = {
            "replicas_desired": deployment.spec.replicas,
            "replicas_ready": deployment.status.ready_replicas,
            "replicas_updated": deployment.status.updated_replicas,
            "available_replicas": deployment.status.available_replicas
        }

        # 3. Specifiche del Container (Immagine)
        # Prende il primo container definito nel template del pod
        image_spec = deployment.spec.template.spec.containers[0]
        container_details = {
            "container_name": image_spec.name,
            "image": image_spec.image,
            "ports": [p.container_port for p in image_spec.ports] if image_spec.ports else "N/D"
        }
        
        # Assembla l'output
        export_data = {
            "metadata": metadata,
            "status": status,
            "container": container_details,
            # Puoi esportare l'intero oggetto come JSON se necessario:
            # "full_spec": deployment.to_dict() 
        }

        print("\n--- Dettagli Deployment Esportati ---")
        print(json.dumps(export_data, indent=2))
        
    except client.ApiException as e:
        # Gestisce gli errori, ad esempio "Forbidden" se il Service Account non ha permessi sufficienti
        print(f"Errore durante l'accesso al Deployment: {e}")
        print(f"Verifica che il Service Account 'cluster-reader' abbia i permessi di lettura su Deployment nel namespace {NAMESPACE}.")
        

if __name__ == "__main__":
    export_deployment_details()
