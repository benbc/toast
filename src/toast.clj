(ns toast
  (:use compojure.core
        ring.adapter.jetty
        hiccup.core)
  (:gen-class))

(defn error-404 [body]
  {:status 404, :body body})

(defroutes main-routes
  (GET "/" []
       (html [:h1 "Here is the thing"]))
  (ANY "*" []
       (error-404 (html [:h1 "Doh!"]))))

(defn -main [& args]
  (run-jetty main-routes {:port 8080}))
