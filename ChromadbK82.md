 # Check deployment status
   kubectl get all -n chromadb
   
   # View logs
   kubectl logs -f -n chromadb -l app=chromadb
   
   # Scale deployment
   kubectl scale deployment chromadb -n chromadb --replicas=2
   
   # Delete deployment
   kubectl delete namespace chromadb

   # check 
      kubectl get ingressroute -n chromadb
      