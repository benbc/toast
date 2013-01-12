(ns toast.main
  (:use ring.adapter.jetty)
  (:require [toast.handler :as handler])
  (:gen-class))

(defn -main []
  (run-jetty handler/app {:port 80}))
