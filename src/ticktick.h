#pragma once

#include "stdafx.h"
#include "config.h"


namespace tickout
{
    using std::string;

    class ticktick_t
    {
    public:
        const string api_base = "";
        const inline void setup(string& path) {this->config_.read(path);}

    protected:
        void configure_requester(URLpp::Easy& request) const
        {
            request.setOpt(new curlpp::options::FollowLocation(true));
            request.setOpt(new curlpp::options::UserAgent(this->config_.user_agent()));

            request.setOpt(new cURLpp::options::Timeout(this->config_.read_timeout()));

            if (this->config_.proxy())
                request.setOpt(new cURLpp::options::Proxy(this->config_.proxy_address()));

            if (this->config_.verbose())
                request.setOpt(new curlpp::options::Verbose(true));
        };

    private:
        ticktick_t() = default;

        config config_;
        string client_id_;
        string client_secret_;

    };
    
}
