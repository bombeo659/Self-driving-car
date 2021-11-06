
(cl:in-package :asdf)

(defsystem "rj_training-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "StringWithHeader" :depends-on ("_package_StringWithHeader"))
    (:file "_package_StringWithHeader" :depends-on ("_package"))
  ))