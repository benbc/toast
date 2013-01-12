(ns toast.deploy
  (:gen-class))

(defn ensure-bucket-exists [])
(defn upload-jar [])

(defn upload-artifacts []
  (ensure-bucket-exists)
  (upload-jar))

(defn stack-exists? [])
(defn create-stack [])
(defn update-stack [])

(defn deploy-system []
  (if (stack-exists?)
    (update-stack)
    (create-stack)))

(defn -main []
  (upload-artifacts)
  (deploy-system))
