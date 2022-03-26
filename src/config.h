#pragma once


#ifndef TICKOUT_CONFIG_H
#define TICKOUT_CONFIG_H

#include "stdafx.h"

using json = nlohmann::json;

namespace tickout
{
    const std::string default_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0";

    class config
    {
    public:
        config()               = default;
        config(const config&)  = default;  // Copy constructor
        config(config&&)       = default;  // Move constructor
        ~config()              = default;
        config& operator= (const config&) = default;  // Copy assignment operator
        config& operator= (config&&)      = default;  // Move assignment operator

        void read(const std::string&);

        auto proxy() const { return this->proxy_; }
        auto proxy_address() const { return this->proxy_address_; }
        auto user_agent() const { return this->user_agent_; }
        auto chdir() const { return this->chdir_; }

        auto verbose() const { return this->verbose_; }
        void set_verbose(const bool mode)
        {
            this->verbose_ = mode;
        }

        auto read_timeout() const { return this->read_timeout_; }

        auto bind() const { return this->bind_; }
        auto port() const { return this->port_; }

    protected:
        bool proxy_ = false;
        std::string proxy_address_;
        std::string user_agent_ = default_user_agent;
        std::string chdir_;
        bool verbose_ = false;

        std::string client_id_;
        std::string client_secret_;

        unsigned int read_timeout_ = 60;  // 1 minute by default;
        std::string bind_ = "127.0.0.1";
        int16_t port_ = 8000;
    };
}

#endif  // TICKOUT_CONFIG_H
