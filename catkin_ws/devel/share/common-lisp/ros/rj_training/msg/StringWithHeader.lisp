; Auto-generated. Do not edit!


(cl:in-package rj_training-msg)


;//! \htmlinclude StringWithHeader.msg.html

(cl:defclass <StringWithHeader> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (data
    :reader data
    :initarg :data
    :type cl:string
    :initform ""))
)

(cl:defclass StringWithHeader (<StringWithHeader>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <StringWithHeader>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'StringWithHeader)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rj_training-msg:<StringWithHeader> is deprecated: use rj_training-msg:StringWithHeader instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <StringWithHeader>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rj_training-msg:header-val is deprecated.  Use rj_training-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'data-val :lambda-list '(m))
(cl:defmethod data-val ((m <StringWithHeader>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rj_training-msg:data-val is deprecated.  Use rj_training-msg:data instead.")
  (data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <StringWithHeader>) ostream)
  "Serializes a message object of type '<StringWithHeader>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'data))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'data))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <StringWithHeader>) istream)
  "Deserializes a message object of type '<StringWithHeader>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'data) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'data) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<StringWithHeader>)))
  "Returns string type for a message object of type '<StringWithHeader>"
  "rj_training/StringWithHeader")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'StringWithHeader)))
  "Returns string type for a message object of type 'StringWithHeader"
  "rj_training/StringWithHeader")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<StringWithHeader>)))
  "Returns md5sum for a message object of type '<StringWithHeader>"
  "c99a9440709e4d4a9716d55b8270d5e7")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'StringWithHeader)))
  "Returns md5sum for a message object of type 'StringWithHeader"
  "c99a9440709e4d4a9716d55b8270d5e7")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<StringWithHeader>)))
  "Returns full string definition for message of type '<StringWithHeader>"
  (cl:format cl:nil "std_msgs/Header header~%string data~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'StringWithHeader)))
  "Returns full string definition for message of type 'StringWithHeader"
  (cl:format cl:nil "std_msgs/Header header~%string data~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <StringWithHeader>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4 (cl:length (cl:slot-value msg 'data))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <StringWithHeader>))
  "Converts a ROS message object to a list"
  (cl:list 'StringWithHeader
    (cl:cons ':header (header msg))
    (cl:cons ':data (data msg))
))
