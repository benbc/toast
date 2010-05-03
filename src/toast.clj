(ns toast
  (:use compojure.core
        ring.adapter.jetty
        hiccup.core)
  (:gen-class))

(def state (atom 0))

(defn error-404 [body]
  {:status 404, :body body})

(defroutes main-routes
  (GET "/" []
       (swap! state + 1)
       (html [:h1 "Here is the thing"] [:p @state]))
  (ANY "*" []
       (error-404 (html [:h1 "Doh!"]))))

(defn -main [& args]
  (run-jetty main-routes {:port 8080}))
